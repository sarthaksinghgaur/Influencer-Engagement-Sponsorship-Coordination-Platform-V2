from celery import shared_task
from models import User, Role, Sponsor, Influencer, Campaign, AdRequest
from mailer_sending import send_email
from jinja2 import Template
from datetime import datetime, timedelta


@shared_task(ignore_result=False)
def monthly_reminder_admin():
    admin_role = Role.query.filter_by(name='admin').first()
    admin = User.query.filter(User.roles.contains(admin_role)).first()

    if not admin:
        print("No admin user found.")
        return "No admin user found."

    with open('report_admin.html', 'r') as file:
        template = Template(file.read())

    # Gather data for the report
    active_users = User.query.filter_by(active=True).count()
    total_campaigns = Campaign.query.count()
    public_campaigns = Campaign.query.filter_by(visibility='public').count()
    private_campaigns = Campaign.query.filter_by(visibility='private').count()
    ad_requests = AdRequest.query.count()
    flagged_sponsors = Sponsor.query.filter_by(flagged=True).count()
    flagged_influencers = Influencer.query.filter_by(flagged=True).count()

    pending_ad_requests = AdRequest.query.filter(
        AdRequest.status.in_(['Negotiations Underway from Sponsor', 'Negotiations Underway from Influencer', 'Influencer Requested for Ad', 'Available'])
    ).count()
    accepted_ad_requests = AdRequest.query.filter_by(status='Accepted').count()

    pending_sponsors = Sponsor.query.filter_by(is_approved=False).all()

    stats = {
        'active_users': active_users,
        'total_campaigns': total_campaigns,
        'public_campaigns': public_campaigns,
        'private_campaigns': private_campaigns,
        'ad_requests': ad_requests,
        'flagged_sponsors': flagged_sponsors,
        'flagged_influencers': flagged_influencers,
        'pending_ad_requests': pending_ad_requests,
        'accepted_ad_requests': accepted_ad_requests,
        'sponsors': pending_sponsors
    }

    email_content = template.render(
        active_users=stats['active_users'],
        total_campaigns=stats['total_campaigns'],
        public_campaigns=stats['public_campaigns'],
        private_campaigns=stats['private_campaigns'],
        ad_requests=stats['ad_requests'],
        flagged_sponsors=stats['flagged_sponsors'],
        flagged_influencers=stats['flagged_influencers'],
        accepted_ad_requests=stats['accepted_ad_requests'],
        sponsors=stats['sponsors']
    )

    send_email(
        admin.email,
        "Monthly Admin Report",
        email_content
    )
    return "Monthly report sent to admin."


@shared_task(ignore_result=False)
def monthly_reminder_sponsors():
    sponsors = Sponsor.query.all()

    with open('report_sponsor.html', 'r') as file:
        template = Template(file.read())

    for sponsor in sponsors:
        sponsor_campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
        ad_requests = AdRequest.query.filter_by(sponsor_id=sponsor.id).all()

        # Calculate budget used and remaining
        total_campaign_budget = sum(campaign.budget for campaign in sponsor_campaigns)
        budget_used = sum(request.payment_amount for request in ad_requests if request.status == 'Accepted')
        budget_remaining = sponsor.budget - budget_used

        stats = {
            'company_name': sponsor.company_name,
            'total_campaigns': len(sponsor_campaigns),
            'ad_requests': len(ad_requests),
            'budget_used': budget_used,
            'budget_remaining': budget_remaining,
            'campaigns': sponsor_campaigns,
            'ad_requests_list': ad_requests
        }

        email_content = template.render(
            company_name=stats['company_name'],
            total_campaigns=stats['total_campaigns'],
            ad_requests=stats['ad_requests'],
            budget_used=stats['budget_used'],
            budget_remaining=stats['budget_remaining'],
            campaigns=stats['campaigns'],
            ad_requests_list=stats['ad_requests_list']
        )

        # Send the email to each sponsor
        send_email(
            sponsor.user.email,
            "Monthly Campaign Report",
            email_content
        )

    return "Monthly reports sent to all sponsors."


from json import dumps
from httplib2 import Http

@shared_task(ignore_result=False)
def daily_reminder_influencer():
    try:
        # Get influencers who haven't logged in within the past 24 hours
        timestamp = datetime.utcnow() - timedelta(hours=24)

        # Get users with associated influencer accounts who haven't logged in in the last 24 hours
        not_visited_influencers = User.query.filter(
            User.influencer != None,  # Ensure that the user has an associated Influencer record
            User.last_login_at < timestamp
        ).all()

        # Get influencers with pending ad requests
        pending_ad_requests = AdRequest.query.filter(
            AdRequest.status.in_([
                'Negotiations Underway from Sponsor',
                'Negotiations Underway from Influencer',
                'Available',
                'Requested Ad for Influencer'
            ])
        ).all()

        # Get a set of influencer user IDs with pending ad requests
        pending_influencer_ids = {ad.influencer.user_id for ad in pending_ad_requests if ad.influencer_id}

        # Get users who have pending ad requests
        influencers_with_pending_requests = User.query.filter(
            User.influencer != None,
            User.id.in_(pending_influencer_ids)
        ).all()

        # Combine both sets of influencers without duplication
        all_influencers_to_notify = set(not_visited_influencers + influencers_with_pending_requests)

        if not all_influencers_to_notify:
            return "No influencers to notify today"

        for user in all_influencers_to_notify:
            if user.username != 'admin':  # Ensure admin is not notified
                send_notification(user.username)
                send_email_notification(user.email)

        return "Notifications sent to Google Chat and via email"
    except Exception as e:
        print(f"Error in daily_reminder task: {e}")
        return f"Error in daily_reminder task: {e}"



def send_notification(username):
    try:
        url = "https://chat.googleapis.com/v1/spaces/AAAABTv-Va8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Q8gas2L22tGg9qYOHI1ovW0-hadv12Nam_qG7g8_BRg"
        app_message = {"text": f"Hello {username}! You haven't visited the IESCP V2 app today or you have pending ad requests. Please log in to check public Ad Requests and take action on your Ad Requests."}
        message_headers = {"Content-Type": "application/json; charset=UTF-8"}
        http_obj = Http()
        response = http_obj.request(
            uri=url,
            method="POST",
            headers=message_headers,
            body=dumps(app_message),
        )
        return f"Notification sent to {username}"
    except Exception as e:
        print(f"Error in send_notification task: {e}")
        return f"Error in send_notification task: {e}"
    
def send_email_notification(email):
    try:
        subject = "Daily Reminder: Pending Ad Requests or Inactivity"
        content = "Hello! You either haven't logged in to IESCP V2 today or you have pending ad requests. Please visit the platform and take necessary actions."
        send_email(email, subject, content)
    except Exception as e:
        print(f"Error sending email notification: {e}")
from celery import shared_task
from models import User, Role, Sponsor, Influencer, Campaign, AdRequest
import flask_excel as excel
from mailer_sending import send_email
from jinja2 import Template
from datetime import datetime, timedelta


@shared_task(ignore_result=False)
def monthly_reminder():
    admin_role = Role.query.filter_by(name='admin').first()

    admin = User.query.filter(User.roles.contains(admin_role)).first()

    if not admin:
        print("No admin user found.")
        return "No admin user found."

    with open('report.html', 'r') as file:
        template = Template(file.read())
        
    active_users = User.query.filter_by(active=True).count()
    total_campaigns = Campaign.query.count()
    public_campaigns = Campaign.query.filter_by(visibility='public').count()
    private_campaigns = Campaign.query.filter_by(visibility='private').count()
    ad_requests = AdRequest.query.count()
    flagged_sponsors = Sponsor.query.filter_by(flagged=True).count()
    flagged_influencers = Influencer.query.filter_by(flagged=True).count()

    pending_ad_requests = AdRequest.query.filter(
        AdRequest.status.in_(['Negotiations Underway from Sponsor', 'Negotiations Underway from influencer'])
    ).count()
    accepted_ad_requests = AdRequest.query.filter_by(status='Accepted').count()
    rejected_ad_requests = AdRequest.query.filter_by(status='Rejected').count()

    pending_sponsors = Sponsor.query.filter_by(is_approved=False).all()

    sponsors = Sponsor.query.all()
    influencers = Influencer.query.all()
    campaigns = Campaign.query.all()

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
        'rejected_ad_requests': rejected_ad_requests,
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
        pending_ad_requests=stats['pending_ad_requests'],
        accepted_ad_requests=stats['accepted_ad_requests'],
        rejected_ad_requests=stats['rejected_ad_requests'],
        sponsors=stats['sponsors']
    )
   
    send_email(
        admin.email,
        "Monthly Report",
        email_content
    )
    return "Monthly report sent to admin."


from json import dumps
from httplib2 import Http



@shared_task(ignore_result=False)
def daily_reminder():
    try:
  
        timestamp = datetime.utcnow() - timedelta(hours=24)

        # not_visited_users = User.query.filter(User.last_login_at < timestamp).all()

        not_visited_users = User.query.filter(User.last_login_at < datetime.utcnow()).all()
        if not not_visited_users:
            return "no inactive users today"

        for user in not_visited_users:
            username = user.username
            if username != 'admin':
                send_notification(username)

        return "Notifications sent to google chat space"
    except Exception as e:
        print(f"Error in daily_reminder task: {e}")
        return f"Error in daily_reminder task: {e}"

def send_notification(username):
    try:
        url = "https://chat.googleapis.com/v1/spaces/AAAABTv-Va8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Q8gas2L22tGg9qYOHI1ovW0-hadv12Nam_qG7g8_BRg"
        app_message = {"text": f"Hello {username}! You haven't visited IESCP V2 app today. Try to visit and do some business :D"}
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
from app import create_app
from models import db, user_datastore, User, Role, Influencer, Sponsor, Campaign, AdRequest
from flask_security.utils import hash_password
from datetime import datetime, timedelta

app, _ = create_app()

def create_roles():
    admin_role = Role(name="admin", description="Administrator with full access")
    sponsor_role = Role(name="sponsor", description="Sponsor role for creating campaigns and ad requests")
    influencer_role = Role(name="influencer", description="Influencer role for accepting ad requests")

    db.session.add_all([admin_role, sponsor_role, influencer_role])
    db.session.commit()
    return admin_role, sponsor_role, influencer_role


def create_users(admin_role, sponsor_role, influencer_role):

    admin_user = user_datastore.create_user(
        email="admin@example.com", username="admin", password=hash_password("adminpassword"), active=True
    )
    user_datastore.add_role_to_user(admin_user, admin_role)


    sponsor_user = user_datastore.create_user(
        email="sponsor@example.com", username="sponsor", password=hash_password("sponsorpassword"), active=True
    )
    user_datastore.add_role_to_user(sponsor_user, sponsor_role)


    influencer_user = user_datastore.create_user(
        email="influencer@example.com", username="influencer", password=hash_password("influencerpassword"), active=True
    )
    user_datastore.add_role_to_user(influencer_user, influencer_role)

    db.session.commit()
    return admin_user, sponsor_user, influencer_user


def create_sponsor(sponsor_user):
    sponsor_profile = Sponsor(
        company_name="Sponsor Inc.",
        industry="Technology",
        budget=50000,
        user_id=sponsor_user.id,
        is_approved=True
    )
    db.session.add(sponsor_profile)
    db.session.commit()
    return sponsor_profile


def create_influencer(influencer_user):
    influencer_profile = Influencer(
        name="Influencer One",
        category="Technology",
        niche="Software",
        reach=10000,
        platform="Instagram",
        user_id=influencer_user.id
    )
    db.session.add(influencer_profile)
    db.session.commit()
    return influencer_profile


def create_campaign(sponsor):
    campaign = Campaign(
        name="Tech Launch Campaign",
        description="A campaign to promote new tech products",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        budget=10000,
        visibility="public",
        goals="Increase brand awareness and product sales",
        sponsor_id=sponsor.id
    )
    db.session.add(campaign)
    db.session.commit()
    return campaign


def create_ad_request(campaign, sponsor, influencer):
    ad_request = AdRequest(
        name="Promotional Post",
        messages="Please create a post highlighting our product.",
        requirements="High engagement on social media",
        payment_amount=500,
        status="pending",
        sponsor_id=sponsor.id,
        campaign_id=campaign.id,
        influencer_id=influencer.id
    )
    db.session.add(ad_request)
    db.session.commit()
    return ad_request


def populate_database():
    admin_role, sponsor_role, influencer_role = create_roles()
    admin_user, sponsor_user, influencer_user = create_users(admin_role, sponsor_role, influencer_role)
    sponsor_profile = create_sponsor(sponsor_user)
    influencer_profile = create_influencer(influencer_user)
    campaign = create_campaign(sponsor_profile)
    create_ad_request(campaign, sponsor_profile, influencer_profile)
    print("Sample data added to the database.")


with app.app_context():  
    db.drop_all()
    db.create_all()
    populate_database()
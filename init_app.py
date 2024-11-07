from app import create_app
from models import db, user_datastore
from flask_security.utils import hash_password

app, _ = create_app()

def create_empty_tables():
    db.drop_all()
    db.create_all()

with app.app_context():
    create_empty_tables()
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='sponsor', description='Sponsor')
    user_datastore.find_or_create_role(name='influencer', description='Influencer')
    db.session.commit()

    if not user_datastore.find_user(email="admin@admin.admin"):
        admin_user=user_datastore.create_user(email="admin@admin.admin", password=hash_password("adminpassword"), username="admin", is_approved=True)
        user_datastore.add_role_to_user(admin_user, "admin")

    if not user_datastore.find_user(email="sponsor@sponsor.sponsor"):
        sponsor_user=user_datastore.create_user(email="sponsor@sponsor.sponsor", password=hash_password("sponsorpassword"), username="sponsor", is_approved=False)
        user_datastore.add_role_to_user(sponsor_user, "sponsor")

    if not user_datastore.find_user(email="influencer@influencer.influencer"):
        influencer_user=user_datastore.create_user(email="influencer@influencer.influencer", password=hash_password("influencerpassword"), username="influencer", is_approved=True)
        user_datastore.add_role_to_user(influencer_user, "influencer")
    db.session.commit()
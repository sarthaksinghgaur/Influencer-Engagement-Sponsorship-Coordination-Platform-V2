from flask import Flask
from models import db, user_datastore
from flask_security import Security
from flask_restful import Api
from flask_cors import CORS
from cacher import cache
from celery.schedules import crontab
from celery_task import monthly_reminder_admin, monthly_reminder_sponsors, daily_reminder_influencer
from extensions import mail
from celery_worker import celery_init_app
from cacher import cache

def create_app():
    app = Flask(__name__)
    
    app.config.from_object("config.localDev")
    app.config.from_object("mailer_config.Config")

    db.init_app(app)
    mail.init_app(app)
    
    security = Security(app, user_datastore)

    api = Api(app)

    CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:8080"}})

    cache.init_app(app)

    return app, api

app, api_handler = create_app()

celery_app = celery_init_app(app)

@celery_app.on_after_configure.connect
def celery_job(sender, **kwargs):
    # sender.add_periodic_task( crontab(hour=10, minute=0, day_of_month=1), monthly_reminder_admin.s(), name='monthly_admin_report')
    # sender.add_periodic_task( crontab(hour=10, minute=30, day_of_month=1), monthly_reminder_sponsors.s(), name='monthly_sponsor_report')
    # sender.add_periodic_task(crontab(hour=16, minute=0), daily_reminder_influencer.s(), name='daily_reminder_task')

    sender.add_periodic_task(50, monthly_reminder_admin.s())
    sender.add_periodic_task(50, monthly_reminder_sponsors.s())
    sender.add_periodic_task(50, daily_reminder_influencer.s())

# for demonstration purposes only
@app.route('/clear-cache', methods=['GET'])
def clear_cache():
    cache.clear()
    return "Cache Cleared!" 

from routes.auth import Login, Signup, Logout, SponsorRegistration, InfluencerRegistration
api_handler.add_resource(Login, "/api/login")
api_handler.add_resource(Signup, "/api/signup")
api_handler.add_resource(Logout, "/api/logout")
api_handler.add_resource(SponsorRegistration, '/api/sponsor/register')
api_handler.add_resource(InfluencerRegistration, '/api/influencer/register')

from routes.admin import AdminDashboard, PendingSponsors, ApproveSponsor, AdminViewUsers, AdminViewCampaigns, AdminViewAdRequests, ToggleUserActive, AdminViewSponsors, AdminViewInfluencers, FlagCampaign, FlagSponsor, FlagInfluencer, FlagAdRequest

api_handler.add_resource(AdminDashboard, "/api/admin/AdminDashboard")
api_handler.add_resource(PendingSponsors, "/api/admin/PendingSponsors")
api_handler.add_resource(ApproveSponsor, "/api/admin/ApproveSponsor/<int:sponsor_id>")
api_handler.add_resource(AdminViewUsers, "/api/admin/AdminViewUsers")
api_handler.add_resource(ToggleUserActive, '/api/admin/ToggleUserActive/<int:user_id>')
api_handler.add_resource(AdminViewCampaigns, "/api/admin/AdminViewCampaigns")
api_handler.add_resource(AdminViewAdRequests, "/api/admin/AdminViewAdRequests")
api_handler.add_resource(AdminViewSponsors, "/api/admin/AdminViewSponsors")
api_handler.add_resource(AdminViewInfluencers, "/api/admin/AdminViewInfluencers")
api_handler.add_resource(FlagCampaign, "/api/admin/FlagCampaign/<int:campaign_id>")
api_handler.add_resource(FlagSponsor, "/api/admin/FlagSponsor/<int:sponsor_id>")
api_handler.add_resource(FlagInfluencer, "/api/admin/FlagInfluencer/<int:influencer_id>")
api_handler.add_resource(FlagAdRequest, "/api/admin/FlagAdRequest/<int:ad_request_id>")

from routes.sponsor import SponsorDashboard, CreateCampaign, UpdateCampaign, DeleteCampaign, CreateAdRequest, UpdateAdRequest, DeleteAdRequest, FindInfluencers, ActionInfluencer

api_handler.add_resource(SponsorDashboard, "/api/sponsor/SponsorDashboard")
api_handler.add_resource(CreateCampaign, "/api/sponsor/CreateCampaign")
api_handler.add_resource(UpdateCampaign, "/api/sponsor/UpdateCampaign/<int:campaign_id>")
api_handler.add_resource(DeleteCampaign, "/api/sponsor/DeleteCampaign/<int:campaign_id>")
api_handler.add_resource(CreateAdRequest, "/api/sponsor/CreateAdRequest")
api_handler.add_resource(UpdateAdRequest, "/api/sponsor/UpdateAdRequest/<int:ad_request_id>")
api_handler.add_resource(DeleteAdRequest, "/api/sponsor/DeleteAdRequest/<int:ad_request_id>")
api_handler.add_resource(FindInfluencers, "/api/sponsor/FindInfluencers")
api_handler.add_resource(ActionInfluencer, "/api/sponsor/ActionInfluencer/<int:influencer_id>")

from routes.influencer import InfluencerDashboard, ActionAdRequest, FindCampaigns, FindAdRequests, UpdateInfluencerProfile

api_handler.add_resource(InfluencerDashboard, "/api/influencer/InfluencerDashboard")
api_handler.add_resource(ActionAdRequest, "/api/influencer/ActionAdRequest/<int:id>")
api_handler.add_resource(FindCampaigns, "/api/influencer/FindCampaigns")
api_handler.add_resource(FindAdRequests, "/api/influencer/FindAdRequests/<int:campaign_id>")
api_handler.add_resource(UpdateInfluencerProfile, "/api/influencer/UpdateInfluencerProfile")

from routes.export import export_bp
app.register_blueprint(export_bp, url_prefix='/api/export')

if __name__ == "__main__":
    app.run(port=8008, debug=True)
from flask import request

def create_app():
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object("config.localDev")

    from models import db, user_datastore

    db.init_app(app)
    
    from flask_security import Security
    security = Security(app, user_datastore)

    from flask_restful import Api
    api = Api(app)

    from flask_cors import CORS
    CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:8080"}})

    from flask_caching import Cache
    cache = Cache(app)

    return app, api

app, api_handler = create_app()

from routes.hello_worldo import hello_worldo  
api_handler.add_resource(hello_worldo, "/hello_worldo")

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

if __name__ == "__main__":
    app.run(port=8008, debug=True)
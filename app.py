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
    CORS(app)

    return app, api

app, api_handler = create_app()


@app.route("/hello_worldo")
def hello_world():
    return "Hello Worldo!"

from routes.testooo import test0  
api_handler.add_resource(test0, "/testo")

from routes.auth import Signin, Signup, Logout
api_handler.add_resource(Signin, "/api/signin")
api_handler.add_resource(Signup, "/api/signup")
api_handler.add_resource(Logout, "/api/logout")

from routes.admin import AdminDashboard, PendingSponsors, ApproveSponsor, AdminViewUsers, AdminViewCampaigns, AdminViewAdRequests, AdminViewSponsors, AdminViewInfluencers, AdminEditUser, AdminEditCampaign, AdminEditAdRequest, AdminEditSponsor, AdminEditInfluencer, AdminDeleteUser, AdminDeleteCampaign, AdminDeleteAdRequest, AdminDeleteSponsor, AdminDeleteInfluencer

api_handler.add_resource(AdminDashboard, "/api/admin/AdminDashboard")
api_handler.add_resource(PendingSponsors, "/api/admin/PendingSponsors")
api_handler.add_resource(ApproveSponsor, "/api/admin/ApproveSponsor/<int:sponsor_id>")
api_handler.add_resource(AdminViewUsers, "/api/admin/AdminViewUsers")
api_handler.add_resource(AdminViewCampaigns, "/api/admin/AdminViewCampaigns")
api_handler.add_resource(AdminViewAdRequests, "/api/admin/AdminViewAdRequests")
api_handler.add_resource(AdminViewSponsors, "/api/admin/AdminViewSponsors")
api_handler.add_resource(AdminViewInfluencers, "/api/admin/AdminViewInfluencers")
api_handler.add_resource(AdminEditUser, "/api/admin/AdminEditUser/<int:user_id>")
api_handler.add_resource(AdminEditCampaign, "/api/admin/AdminEditCampaign/<int:campaign_id>")
api_handler.add_resource(AdminEditAdRequest, "/api/admin/AdminEditAdRequest/<int:ad_request_id>")
api_handler.add_resource(AdminEditSponsor, "/api/admin/AdminEditSponsor/<int:sponsor_id>")
api_handler.add_resource(AdminEditInfluencer, "/api/admin/AdminEditInfluencer/<int:influencer_id>")
api_handler.add_resource(AdminDeleteUser, "/api/admin/AdminDeleteUser/<int:user_id>")
api_handler.add_resource(AdminDeleteCampaign, "/api/admin/AdminDeleteCampaign/<int:campaign_id>")
api_handler.add_resource(AdminDeleteAdRequest, "/api/admin/AdminDeleteAdRequest/<int:ad_request_id>")
api_handler.add_resource(AdminDeleteSponsor, "/api/admin/AdminDeleteSponsor/<int:sponsor_id>")
api_handler.add_resource(AdminDeleteInfluencer, "/api/admin/AdminDeleteInfluencer/<int:influencer_id>")

from routes.influencer import InfluencerDashboard, ActionAdRequest, FindCampaigns, FindAdRequests, FindInfluencers, UpdateInfluencerProfile, ActionInfluencer

api_handler.add_resource(InfluencerDashboard, "/api/influencer/InfluencerDashboard")
api_handler.add_resource(ActionAdRequest, "/api/influencer/ActionAdRequest/<int:id>")
api_handler.add_resource(FindCampaigns, "/api/influencer/FindCampaigns")
api_handler.add_resource(FindAdRequests, "/api/influencer/FindAdRequests/<int:campaign_id>")
api_handler.add_resource(FindInfluencers, "/api/influencer/FindInfluencers")
api_handler.add_resource(UpdateInfluencerProfile, "/api/influencer/UpdateInfluencerProfile")
api_handler.add_resource(ActionInfluencer, "/api/influencer/ActionInfluencer/<int:influencer_id>")

from routes.sponsor import SponsorDashboard, CreateCampaign, EditCampaign, DeleteCampaign, CreateAdRequest, EditAdRequest, DeleteAdRequest

api_handler.add_resource(SponsorDashboard, "/api/sponsor/SponsorDashboard")
api_handler.add_resource(CreateCampaign, "/api/sponsor/CreateCampaign")
api_handler.add_resource(EditCampaign, "/api/sponsor/EditCampaign/<int:campaign_id>")
api_handler.add_resource(DeleteCampaign, "/api/sponsor/DeleteCampaign/<int:campaign_id>")
api_handler.add_resource(CreateAdRequest, "/api/sponsor/CreateAdRequest")
api_handler.add_resource(EditAdRequest, "/api/sponsor/EditAdRequest/<int:ad_request_id>")
api_handler.add_resource(DeleteAdRequest, "/api/sponsor/DeleteAdRequest/<int:ad_request_id>")



if __name__ == "__main__":
    app.run(port=8008, debug=True)
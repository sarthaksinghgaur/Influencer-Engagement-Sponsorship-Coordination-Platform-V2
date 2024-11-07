from flask import jsonify, request, session, redirect, make_response
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted, roles_required
from models import *

class AdminDashboard(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        active_users = User.query.filter_by(active=True).count()
        total_campaigns = Campaign.query.count()
        public_campaigns = Campaign.query.filter_by(visibility='public').count()
        private_campaigns = Campaign.query.filter_by(visibility='private').count()
        ad_requests = AdRequest.query.count()
        flagged_sponsors = Sponsor.query.filter_by(flagged=True).count()
        flagged_influencers = Influencer.query.filter_by(flagged=True).count()

        # Fetch AdRequest statistics
        pending_ad_requests = AdRequest.query.filter(
            AdRequest.status.in_(['Negotiations Underway from Sponsor', 'Negotiations Underway from influencer'])
        ).count()
        accepted_ad_requests = AdRequest.query.filter_by(status='Accepted').count()
        rejected_ad_requests = AdRequest.query.filter_by(status='Rejected').count()

        # Fetch all sponsors and influencers
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
            'rejected_ad_requests': rejected_ad_requests
        }

        return jsonify({
            'stats': stats,
            'campaigns': [{'id': campaign.id, 'name': campaign.name} for campaign in campaigns],
            'sponsors': [{'id': sponsor.id, 'name': sponsor.name} for sponsor in sponsors],
            'influencers': [{'id': influencer.id, 'name': influencer.name} for influencer in influencers]
        })

class PendingSponsors(Resource):
    @roles_required('admin')
    def get(self):
        pending_sponsors = User.query.join(RolesUsers).join(Role).filter(Role.name == 'sponsor', User.is_approved == False).all()
        sponsors_data = [
            {
                "id": sponsor.id,
                "email": sponsor.email,
                "username": sponsor.username
            }
            for sponsor in pending_sponsors
        ]
        return make_response(jsonify({"pending_sponsors": sponsors_data}), 200)

class ApproveSponsor(Resource):
    @roles_required('admin')
    def post(self, sponsor_id):
        sponsor = User.query.filter_by(id=sponsor_id, is_approved=False).first()
        if not sponsor:
            return make_response(jsonify({"message": "Sponsor not found or already approved"}), 404)
        
        sponsor.is_approved = True
        db.session.commit()
        
        return make_response(jsonify({"message": "Sponsor has been approved", "email": sponsor.email}), 200)

class AdminViewUsers(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        users = User.query.all()
        users_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        return jsonify(users_data)

class AdminViewCampaigns(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        campaigns = Campaign.query.all()
        campaigns_data = [{'id': campaign.id, 'name': campaign.name, 'visibility': campaign.visibility} for campaign in campaigns]
        return jsonify(campaigns_data)

class AdminViewAdRequests(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        ad_requests = AdRequest.query.all()
        ad_requests_data = [{'id': ad_request.id, 'status': ad_request.status, 'campaign_id': ad_request.campaign_id} for ad_request in ad_requests]
        return jsonify(ad_requests_data)
    
class AdminViewSponsors(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        sponsors = Sponsor.query.all()
        sponsors_data = [{'id': sponsor.id, 'name': sponsor.name, 'flagged': sponsor.flagged} for sponsor in sponsors]
        return jsonify(sponsors_data)
    
class AdminViewInfluencers(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        influencers = Influencer.query.all()
        influencers_data = [{'id': influencer.id, 'name': influencer.name, 'flagged': influencer.flagged} for influencer in influencers]
        return jsonify(influencers_data)
    
class AdminEditUser(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        user_data = {'id': user.id, 'username': user.username, 'email': user.email, 'active': user.active, 'role': user.role}
        return jsonify(user_data)

    @auth_token_required
    @roles_accepted('admin')
    def post(self, user_id):
        user = User.query.get_or_404(user_id)
        user.username = request.form['username']
        user.email = request.form['email']
        user.active = 'active' in request.form
        user.role = request.form['role']
        db.session.commit()
        return jsonify({'message': 'User updated successfully!'})
    
class AdminEditCampaign(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        campaign_data = {
            'id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'start_date': campaign.start_date.strftime('%Y-%m-%d'),
            'end_date': campaign.end_date.strftime('%Y-%m-%d'),
            'budget': campaign.budget,
            'visibility': campaign.visibility
        }
        return jsonify(campaign_data)

    @auth_token_required
    @roles_accepted('admin')
    def post(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        campaign.name = request.form['name']
        campaign.description = request.form['description']
        campaign.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        campaign.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        campaign.budget = request.form['budget']
        campaign.visibility = request.form['visibility']
        db.session.commit()
        return jsonify({'message': 'Campaign updated successfully!'})

class AdminEditAdRequest(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        ad_request_data = {
            'id': ad_request.id,
            'name': ad_request.name,
            'messages': ad_request.messages,
            'requirements': ad_request.requirements,
            'payment_amount': ad_request.payment_amount,
            'status': ad_request.status
        }
        return jsonify(ad_request_data)

    @auth_token_required
    @roles_accepted('admin')
    def post(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        ad_request.name = request.form['name']
        ad_request.messages = request.form['messages']
        ad_request.requirements = request.form['requirements']
        ad_request.payment_amount = request.form['payment_amount']
        ad_request.status = request.form['status']
        db.session.commit()
        return jsonify({'message': 'Ad request updated successfully!'})
    
class AdminEditSponsor(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self, sponsor_id):
        sponsor = Sponsor.query.get_or_404(sponsor_id)
        sponsor_data = {
            'id': sponsor.id,
            'company_name': sponsor.company_name,
            'industry': sponsor.industry,
            'budget': sponsor.budget,
            'flagged': sponsor.flagged
        }
        return jsonify(sponsor_data)

    @auth_token_required
    @roles_accepted('admin')
    def post(self, sponsor_id):
        sponsor = Sponsor.query.get_or_404(sponsor_id)
        sponsor.company_name = request.form['company_name']
        sponsor.industry = request.form['industry']
        sponsor.budget = request.form['budget']
        sponsor.flagged = 'flagged' in request.form
        db.session.commit()
        return jsonify({'message': 'Sponsor updated successfully!'})
    
class AdminEditInfluencer(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self, influencer_id):
        influencer = Influencer.query.get_or_404(influencer_id)
        influencer_data = {
            'id': influencer.id,
            'name': influencer.name,
            'category': influencer.category,
            'niche': influencer.niche,
            'reach': influencer.reach,
            'platform': influencer.platform,
            'flagged': influencer.flagged
        }
        return jsonify(influencer_data)

    @auth_token_required
    @roles_accepted('admin')
    def post(self, influencer_id):
        influencer = Influencer.query.get_or_404(influencer_id)
        influencer.name = request.form['name']
        influencer.category = request.form['category']
        influencer.niche = request.form['niche']
        influencer.reach = request.form['reach']
        influencer.platform = request.form['platform']
        influencer.flagged = 'flagged' in request.form
        db.session.commit()
        return jsonify({'message': 'Influencer updated successfully!'})
    
class AdminDeleteUser(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully!'})
    
class AdminDeleteCampaign(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def delete(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        db.session.delete(campaign)
        db.session.commit()
        return jsonify({'message': 'Campaign deleted successfully!'})

class AdminDeleteAdRequest(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def delete(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        db.session.delete(ad_request)
        db.session.commit()
        return jsonify({'message': 'Ad request deleted successfully!'})
    
class AdminDeleteSponsor(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def delete(self, sponsor_id):
        sponsor = Sponsor.query.get_or_404(sponsor_id)
        db.session.delete(sponsor)
        db.session.commit()
        return jsonify({'message': 'Sponsor deleted successfully!'})
    
class AdminDeleteInfluencer(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def delete(self, influencer_id):
        influencer = Influencer.query.get_or_404(influencer_id)
        db.session.delete(influencer)
        db.session.commit()
        return jsonify({'message': 'Influencer deleted successfully!'})
from flask import jsonify, session, request
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted
from models import *

class InfluencerDashboard(Resource):
    @auth_token_required
    @roles_accepted('influencer')
    def get(self):
        user = User.query.get(session['user_id'])
        if not user or user.role != 'influencer':
            return jsonify({'message': 'You do not have permission to access the influencer dashboard.'}), 403

        influencer = Influencer.query.filter_by(user_id=user.id).first()
        if not influencer:
            return jsonify({'message': 'Please complete your influencer registration.'}), 400

        ad_requests = AdRequest.query.filter_by(influencer_id=influencer.id).all()
        campaign_ids = {ad_request.campaign_id for ad_request in ad_requests}
        campaigns = Campaign.query.filter(Campaign.id.in_(campaign_ids)).all()

        return jsonify({
            'user': {'id': user.id, 'username': user.username, 'role': user.role},
            'influencer': {'id': influencer.id, 'name': influencer.name},
            'ad_requests': [{'id': ad_request.id, 'status': ad_request.status} for ad_request in ad_requests],
            'campaigns': [{'id': campaign.id, 'name': campaign.name} for campaign in campaigns]
        })
    
class ActionAdRequest(Resource):
    @auth_token_required
    @roles_accepted('influencer')
    def get(self, id):
        ad_request = AdRequest.query.get_or_404(id)
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
    @roles_accepted('influencer')
    def post(self, id):
        ad_request = AdRequest.query.get_or_404(id)
        action = request.form['action']
        if action == 'accept':
            ad_request.status = 'Accepted'
        elif action == 'reject':
            ad_request.status = 'Rejected'
        elif action == 'negotiate':
            new_payment_amount = request.form['new_payment_amount']
            ad_request.payment_amount = new_payment_amount
            ad_request.status = 'Negotiations Underway from influencer'
        
        influencer = Influencer.query.filter_by(user_id=session['user_id']).first()
        ad_request.influencer_id = influencer.id
        db.session.commit()
        return jsonify({'message': 'Action taken successfully!'})
    
class FindCampaigns(Resource):
    @auth_token_required
    @roles_accepted('influencer')
    def get(self):
        return jsonify({'message': 'Render the campaign search form here.'})

    @auth_token_required
    @roles_accepted('influencer')
    def post(self):
        name = request.form.get('name')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        budget = request.form.get('budget')

        query = Campaign.query.filter_by(visibility='public')
        
        if name:
            query = query.filter(Campaign.name.ilike(f'%{name}%'))
        if start_date:
            query = query.filter(Campaign.start_date >= start_date)
        if end_date:
            query = query.filter(Campaign.end_date <= end_date)
        if budget:
            query = query.filter(Campaign.budget <= budget)

        campaigns = query.all()
        campaign_data = [{'id': campaign.id, 'name': campaign.name, 'start_date': campaign.start_date, 'end_date': campaign.end_date, 'budget': campaign.budget} for campaign in campaigns]

        return jsonify(campaign_data)
    
class FindAdRequests(Resource):
    @auth_token_required
    @roles_accepted('influencer')
    def get(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        ad_requests = AdRequest.query.filter_by(campaign_id=campaign_id, status='Available').all()
        ad_request_data = [{'id': ad_request.id, 'name': ad_request.name, 'messages': ad_request.messages, 'requirements': ad_request.requirements, 'payment_amount': ad_request.payment_amount} for ad_request in ad_requests]
        
        return jsonify({
            'campaign': {'id': campaign.id, 'name': campaign.name, 'description': campaign.description},
            'ad_requests': ad_request_data
        })

class FindInfluencers(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def get(self):
        return jsonify({'message': 'Render the influencer search form here.'})

    @auth_token_required
    @roles_accepted('sponsor')
    def post(self):
        name = request.form.get('name')
        category = request.form.get('category')
        niche = request.form.get('niche')
        reach = request.form.get('reach')

        query = Influencer.query
        if name:
            query = query.filter(Influencer.name.ilike(f'%{name}%'))
        if category:
            query = query.filter(Influencer.category.ilike(f'%{category}%'))
        if niche:
            query = query.filter(Influencer.niche.ilike(f'%{niche}%'))
        if reach:
            query = query.filter(Influencer.reach >= reach)

        influencers = query.all()
        influencer_data = [{'id': influencer.id, 'name': influencer.name, 'category': influencer.category, 'niche': influencer.niche, 'reach': influencer.reach} for influencer in influencers]

        return jsonify(influencer_data)
    
class UpdateInfluencerProfile(Resource):
    @auth_token_required
    @roles_accepted('influencer')
    def get(self):
        user = User.query.get(session['user_id'])
        influencer = Influencer.query.filter_by(user_id=user.id).first()
        influencer_data = {
            'name': influencer.name,
            'category': influencer.category,
            'niche': influencer.niche,
            'reach': influencer.reach,
            'platform': influencer.platform
        }
        return jsonify(influencer_data)

    @auth_token_required
    @roles_accepted('influencer')
    def post(self):
        user = User.query.get(session['user_id'])
        influencer = Influencer.query.filter_by(user_id=user.id).first()
        influencer.name = request.form['name']
        influencer.category = request.form['category']
        influencer.niche = request.form['niche']
        influencer.reach = request.form['reach']
        influencer.platform = request.form['platform']
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully!'})
    
class ActionInfluencer(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def get(self, influencer_id):
        influencer = Influencer.query.get_or_404(influencer_id)
        user = User.query.get(session['user_id'])
        sponsor = Sponsor.query.filter_by(user_id=user.id).first()
        campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
        ad_requests = AdRequest.query.filter_by(sponsor_id=sponsor.id).all()
        return jsonify({
            'influencer': {'id': influencer.id, 'name': influencer.name},
            'campaigns': [{'id': campaign.id, 'name': campaign.name} for campaign in campaigns],
            'ad_requests': [{'id': ad_request.id, 'name': ad_request.name} for ad_request in ad_requests]
        })

    @auth_token_required
    @roles_accepted('sponsor')
    def post(self, influencer_id):
        ad_request_id = request.form['selected_ad_request_id']
        action = request.form['action']
        
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        ad_request.influencer_id = influencer_id
        ad_request.status = action
        db.session.commit()
        return jsonify({'message': 'Influencer requested for ad request successfully!'})

from flask import jsonify, session, request, make_response
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted
from models import Influencer, AdRequest, Campaign, db
from datetime import datetime
from flask_login import current_user
from cacher import cache

class InfluencerDashboard(Resource):
    @auth_token_required
    @roles_accepted('influencer')
    @cache.cached(timeout=10)
    def get(self):
        user = current_user
        influencer = Influencer.query.filter_by(user_id=user.id).first()
        ad_requests = AdRequest.query.filter_by(influencer_id=influencer.id).all()
        campaign_ids = {ad_request.campaign_id for ad_request in ad_requests}
        campaigns = Campaign.query.filter(Campaign.id.in_(campaign_ids)).all()

        return jsonify({
            'influencer': {
                'id': influencer.id,
                'name': influencer.name,
            },
            'ad_requests': [
                {
                    'id': ad_request.id,
                    'name': ad_request.name,
                    'messages': ad_request.messages,
                    'requirements': ad_request.requirements,
                    'payment_amount': ad_request.payment_amount,
                    'status': ad_request.status
                } for ad_request in ad_requests
            ],
            'campaigns': [
                {
                    'id': campaign.id,
                    'name': campaign.name,
                    'description': campaign.description,
                    'start_date': campaign.start_date.strftime('%Y-%m-%d'),
                    'end_date': campaign.end_date.strftime('%Y-%m-%d'),
                    'budget': campaign.budget
                } for campaign in campaigns
            ]
        })
    
class ActionAdRequest(Resource):
    @auth_token_required
    @roles_accepted('influencer')
    @cache.cached(timeout=10)
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
        user = current_user
        influencer = Influencer.query.filter_by(user_id=user.id).first()

        data = request.get_json()
        action = data['action']

        if action == 'accept':
            ad_request.status = 'Accepted'
            ad_request.influencer_id = influencer.id
        elif action == 'reject':
            ad_request.status = 'Available'
            ad_request.influencer_id = None
        elif action == 'negotiate':
            new_payment_amount = data.get('new_payment_amount')
            if new_payment_amount:
                ad_request.payment_amount = new_payment_amount
                ad_request.status = 'Negotiations Underway from Influencer'
                ad_request.influencer_id = influencer.id

        db.session.commit()
        cache.clear()

        return jsonify({'message': 'Action taken successfully!'})

class FindCampaigns(Resource):
    @auth_token_required
    @roles_accepted('influencer')
    @cache.cached(timeout=10)
    def get(self):
        return jsonify({'message': 'Render the campaign search form here.'})

    @auth_token_required
    @roles_accepted('influencer')
    def post(self):
        data = request.get_json()
        name = data.get('name')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        budget = data.get('budget')

        query = Campaign.query.filter_by(visibility='public', flagged=False)

        if name:
            query = query.filter(Campaign.name.ilike(f'%{name}%'))
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            query = query.filter(Campaign.start_date >= start_date)
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            query = query.filter(Campaign.end_date <= end_date)
        if budget:
            query = query.filter(Campaign.budget <= budget)

        campaigns = query.all()
        campaign_data = [
            {
                'id': campaign.id,
                'name': campaign.name,
                'description': campaign.description,
                'start_date': campaign.start_date.strftime('%Y-%m-%d'),
                'end_date': campaign.end_date.strftime('%Y-%m-%d'),
                'budget': campaign.budget,
                'goals': campaign.goals
            } for campaign in campaigns
        ]
        cache.clear()

        return jsonify(campaign_data)

class FindAdRequests(Resource):
    @auth_token_required
    @roles_accepted('influencer')
    @cache.cached(timeout=10)
    def get(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        ad_requests = AdRequest.query.filter_by(campaign_id=campaign_id, status='Available', flagged=False).all()
        ad_request_data = [
            {
                'id': ad_request.id,
                'name': ad_request.name,
                'messages': ad_request.messages,
                'requirements': ad_request.requirements,
                'payment_amount': ad_request.payment_amount
            } for ad_request in ad_requests
        ]
        
        return jsonify({
            'campaign': {
                'id': campaign.id,
                'name': campaign.name,
                'description': campaign.description
            },
            'ad_requests': ad_request_data
        })


class UpdateInfluencerProfile(Resource):
    @auth_token_required
    @roles_accepted('influencer')
    @cache.cached(timeout=10)
    def get(self):
        user = current_user
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
        user = current_user
        influencer = Influencer.query.filter_by(user_id=user.id).first()
        data = request.get_json()

        influencer.name = data['name']
        influencer.category = data['category']
        influencer.niche = data['niche']
        influencer.reach = data['reach']
        influencer.platform = data['platform']

        db.session.commit()
        cache.clear()
        return jsonify({'message': 'Profile updated successfully!'})



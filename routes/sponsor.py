from flask import jsonify, make_response, request
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted
from models import *
from flask_login import current_user
from datetime import datetime

class SponsorDashboard(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def get(self):
        user = current_user
        sponsor = Sponsor.query.filter_by(user_id=user.id).first()
        campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
        ad_requests = AdRequest.query.filter_by(sponsor_id=sponsor.id).all()

        campaigns_data = [
            {
                'id': campaign.id,
                'name': campaign.name,
                'description': campaign.description,
                'start_date': campaign.start_date,
                'end_date': campaign.end_date,
                'budget': campaign.budget
            } for campaign in campaigns
        ]

        ad_requests_data = [
            {
                'id': ad_request.id,
                'name': ad_request.name,
                'messages': ad_request.messages,
                'payment_amount': ad_request.payment_amount,
                'status': ad_request.status
            } for ad_request in ad_requests
        ]

        return jsonify({
            'sponsor': {'company_name': sponsor.company_name},
            'campaigns': campaigns_data,
            'adRequests': ad_requests_data
        })
    

class CreateCampaign(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        budget = data.get('budget')
        visibility = data.get('visibility')
        goals = data.get('goals')

        if not name or not description or not start_date_str or not end_date_str or not budget or not visibility or not goals:
            return make_response(jsonify({"message": "All fields are required"}), 400)

        user = current_user
        sponsor = Sponsor.query.filter_by(user_id=user.id).first()
        if not sponsor:
            return make_response(jsonify({"message": "Sponsor not found"}), 404)
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        campaign = Campaign(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            visibility=visibility,
            goals=goals,
            sponsor_id=sponsor.id
        )
        db.session.add(campaign)
        db.session.commit()

        return make_response(jsonify({"message": "Campaign created successfully", "campaign_id": campaign.id}), 201)


class UpdateCampaign(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def get(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)

        campaign_data = {
            'id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'start_date': campaign.start_date.strftime('%Y-%m-%d'),
            'end_date': campaign.end_date.strftime('%Y-%m-%d'),
            'budget': campaign.budget,
            'visibility': campaign.visibility,
            'goals': campaign.goals
        }
        return jsonify(campaign_data)

    @auth_token_required
    @roles_accepted('sponsor')
    def post(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        data = request.get_json()

        name = data.get('name')
        description = data.get('description')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        budget = data.get('budget')
        visibility = data.get('visibility')
        goals = data.get('goals')

        if not name or not description or not start_date_str or not end_date_str or not budget or not visibility or not goals:
            return make_response(jsonify({"message": "All fields are required"}), 400)

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        campaign.name = name
        campaign.description = description
        campaign.start_date = start_date
        campaign.end_date = end_date
        campaign.budget = budget
        campaign.visibility = visibility
        campaign.goals = goals

        db.session.commit()

        return jsonify({'message': 'Campaign updated successfully!'})

    
class DeleteCampaign(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def delete(self, campaign_id):
        user = current_user
        sponsor = user.sponsor
        
        campaign = Campaign.query.filter_by(id=campaign_id, sponsor_id=sponsor.id).first()
        if not campaign:
            return make_response(jsonify({'message': 'Campaign not found or unauthorized action.'}), 404)

        ad_requests = campaign.ad_requests
        for ad_request in ad_requests:
            db.session.delete(ad_request)
        
        db.session.delete(campaign)
        db.session.commit()

        return jsonify({'message': 'Campaign and associated ad requests deleted successfully!'})

    

class CreateAdRequest(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def get(self):
        user = current_user
        sponsor = Sponsor.query.filter_by(user_id=user.id).first()

        campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
        campaigns_data = [{'id': campaign.id, 'name': campaign.name} for campaign in campaigns]

        return jsonify({
            'campaigns': campaigns_data
        })

    @auth_token_required
    @roles_accepted('sponsor')
    def post(self):
        data = request.get_json()

        name = data.get('name')
        messages = data.get('messages')
        requirements = data.get('requirements')
        payment_amount = data.get('payment_amount')
        campaign_id = data.get('campaign_id')

        if not name or not messages or not requirements or not payment_amount or not campaign_id:
            return make_response(jsonify({"message": "All fields are required"}), 400)

        user = current_user
        sponsor = Sponsor.query.filter_by(user_id=user.id).first()

        campaign = Campaign.query.filter_by(id=campaign_id, sponsor_id=sponsor.id).first()
        if not campaign:
            return make_response(jsonify({"message": "Invalid campaign ID for the sponsor"}), 400)

        new_ad_request = AdRequest(
            name=name,
            messages=messages,
            requirements=requirements,
            payment_amount=payment_amount,
            status='Available',
            sponsor_id=sponsor.id,
            campaign_id=campaign_id
        )

        db.session.add(new_ad_request)
        db.session.commit()

        return make_response(jsonify({"message": "Ad request created successfully", "ad_request_id": new_ad_request.id}), 201)
    
class UpdateAdRequest(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
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
    @roles_accepted('sponsor')
    def post(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        data = request.get_json()

        name = data.get('name')
        messages = data.get('messages')
        requirements = data.get('requirements')
        payment_amount = data.get('payment_amount')
        status = data.get('status')

        if not name or not messages or not requirements or not payment_amount or not status:
            return make_response(jsonify({"message": "All fields are required"}), 400)

        ad_request.name = name
        ad_request.messages = messages
        ad_request.requirements = requirements
        ad_request.payment_amount = payment_amount
        ad_request.status = status

        db.session.commit()

        return jsonify({'message': 'Ad request updated successfully!'})
    
class DeleteAdRequest(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def delete(self, ad_request_id):
        user = current_user
        sponsor = user.sponsor

        ad_request = AdRequest.query.filter_by(id=ad_request_id, sponsor_id=sponsor.id).first()
        if not ad_request:
            return make_response(jsonify({'message': 'Ad Request not found or unauthorized action.'}), 404)

        db.session.delete(ad_request)
        db.session.commit()

        return jsonify({'message': 'Ad request deleted successfully!'})    


class FindInfluencers(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def post(self):
        data = request.get_json()

        name = data.get('name')
        category = data.get('category')
        niche = data.get('niche')
        reach = data.get('reach')
        platform = data.get('platform')

        query = Influencer.query
        if name:
            query = query.filter(Influencer.name.ilike(f'%{name}%'))
        if category:
            query = query.filter(Influencer.category.ilike(f'%{category}%'))
        if niche:
            query = query.filter(Influencer.niche.ilike(f'%{niche}%'))
        if reach:
            query = query.filter(Influencer.reach >= reach)
        if platform:
            query = query.filter(Influencer.platform.ilike(f'%{platform}%'))

        influencers = query.all()
        influencer_data = [
            {
                'id': influencer.id,
                'name': influencer.name,
                'category': influencer.category,
                'niche': influencer.niche,
                'reach': influencer.reach,
                'platform': influencer.platform,
                'flagged': influencer.flagged
            }
            for influencer in influencers
        ]

        return jsonify(influencer_data)

class ActionInfluencer(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def get(self, influencer_id):
        influencer = Influencer.query.get_or_404(influencer_id)
        user = current_user
        sponsor = Sponsor.query.filter_by(user_id=user.id).first()

        if not sponsor:
            return make_response(jsonify({"message": "Sponsor not found"}), 404)

        ad_requests = AdRequest.query.filter_by(sponsor_id=sponsor.id, status="Available").all()

        return jsonify({
            'influencer': {
                'id': influencer.id,
                'name': influencer.name,
                'category': influencer.category,
                'niche': influencer.niche,
                'reach': influencer.reach,
                'platform': influencer.platform,
                'flagged': influencer.flagged
            },
            'ad_requests': [{'id': ad_request.id, 'name': ad_request.name} for ad_request in ad_requests]
        })

    @auth_token_required
    @roles_accepted('sponsor')
    def post(self, influencer_id):
        data = request.get_json()
        ad_request_id = data.get('selected_ad_request_id')
        action = data.get('action')

        if not ad_request_id or action not in ['request']:
            return make_response(jsonify({"message": "Invalid request data"}), 400)

        ad_request = AdRequest.query.get_or_404(ad_request_id)
 
        if action == 'request':
            ad_request.influencer_id = influencer_id
            ad_request.status = 'Influencer Requested for Ad'

        db.session.commit()
        return jsonify({'message': 'Action taken successfully!'})
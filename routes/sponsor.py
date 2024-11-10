from flask import jsonify, make_response, request
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted
from models import *
from flask_login import current_user

class SponsorDashboard(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def get(self):
        user = current_user
        sponsor = Sponsor.query.filter_by(user_id=user.id).first()

        if not sponsor:
            return jsonify({'message': 'Please complete your sponsor registration.'})
        
        if not sponsor.is_approved:
            return make_response(jsonify({"message": "Your account is pending approval."}), 403)
        
        if sponsor.flagged:
            return make_response(jsonify({"message": "Your account has been flagged."}), 403)

        campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
        ad_requests = AdRequest.query.filter_by(sponsor_id=sponsor.id).all()

        response_data = {
            'sponsor': {'id': sponsor.id, 'company_name': sponsor.company_name},
            'campaigns': [{'id': campaign.id, 'name': campaign.name} for campaign in campaigns],
            'ad_requests': [{'id': ad_request.id, 'status': ad_request.status} for ad_request in ad_requests]
        }
        return make_response(jsonify(response_data), 200)
    
class CreateCampaign(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def get(self):
        return jsonify({'message': 'Render the campaign creation form here.'})

    @auth_token_required
    @roles_accepted('sponsor')
    def post(self):
        data = request.get_json()
        user = current_user
        name = data.get('name')
        description = data.get('description')
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d')
        budget = data.get('budget')
        visibility = data.get('visibility')
        goals = data.get('goals')
        sponsor = Sponsor.query.filter_by(user_id=user.id).first()
        sponsor_id = sponsor.id

        new_campaign = Campaign(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            visibility=visibility,
            goals=goals,
            sponsor_id=sponsor_id
        )
        db.session.add(new_campaign)
        db.session.commit()
        return jsonify({'message': 'Campaign created successfully!'})
    
class EditCampaign(Resource):
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
        campaign.name = data.get('name')
        campaign.description = data.get('description')
        campaign.start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
        campaign.end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d')
        campaign.budget = data.get('budget')
        campaign.visibility = data.get('visibility')
        campaign.goals = data.get('goals')

        db.session.commit()
        return jsonify({'message': 'Campaign updated successfully!'})
    

class DeleteCampaign(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def delete(self, campaign_id):
        user = current_user
        campaign = Campaign.query.get_or_404(campaign_id)
        ad_requests = AdRequest.query.filter_by(campaign_id=campaign_id).all()
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
        return jsonify({
            'campaigns': [{'id': campaign.id, 'name': campaign.name} for campaign in campaigns]
        })

    @auth_token_required
    @roles_accepted('sponsor')
    def post(self):
        user = current_user
        data = request.get_json()
        name = data.get('name')
        requirements = data.get('requirements')
        payment_amount = data.get('payment_amount')
        messages = data.get('messages')
        status = "Available"
        sponsor = Sponsor.query.filter_by(user_id=user.id).first()
        sponsor_id = sponsor.id
        campaign_id = data.get('campaign_id')
        
        new_ad_request = AdRequest(
            name=name,
            messages=messages,
            requirements=requirements,
            payment_amount=payment_amount,
            status=status,
            sponsor_id=sponsor_id,
            campaign_id=campaign_id
        )
        db.session.add(new_ad_request)
        db.session.commit()
        return jsonify({'message': 'Ad request created successfully!'})
    
class EditAdRequest(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def get(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        campaigns = Campaign.query.all()
        influencers = Influencer.query.all()
        ad_request_data = {
            'id': ad_request.id,
            'name': ad_request.name,
            'messages': ad_request.messages,
            'requirements': ad_request.requirements,
            'payment_amount': ad_request.payment_amount,
            'status': ad_request.status,
            'campaigns': [{'id': campaign.id, 'name': campaign.name} for campaign in campaigns],
            'influencers': [{'id': influencer.id, 'name': influencer.name} for influencer in influencers]
        }
        return jsonify(ad_request_data)

    @auth_token_required
    @roles_accepted('sponsor')
    def post(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        data = request.get_json()
        
        ad_request.name = data['name']
        ad_request.messages = data['messages']
        ad_request.requirements = data['requirements']
        ad_request.payment_amount = data['payment_amount']
        ad_request.status = data['status']
        
        db.session.commit()
        return jsonify({'message': 'Ad request updated successfully!'})
    
class DeleteAdRequest(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def delete(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        db.session.delete(ad_request)
        db.session.commit()
        return jsonify({'message': 'Ad request deleted successfully!'})
    


class FindInfluencers(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def get(self):
        return jsonify({'message': 'Render the influencer search form here.'})

    @auth_token_required
    @roles_accepted('sponsor')
    def post(self):
        data = request.get_json()
        name = data.get('name')
        category = data.get('category')
        niche = data.get('niche')
        reach = data.get('reach')

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

class ActionInfluencer(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def get(self, influencer_id):
        influencer = Influencer.query.get_or_404(influencer_id)
        user = current_user
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
        data = request.get_json()
        ad_request_id = data['selected_ad_request_id']
        action = data['action']
        
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        ad_request.influencer_id = influencer_id
        
        if action == 'accept':
            ad_request.status = 'Accepted'
        elif action == 'reject':
            ad_request.status = 'Rejected'
        elif action == 'negotiate':
            new_payment_amount = data['new_payment_amount']
            ad_request.payment_amount = new_payment_amount
            ad_request.status = 'Negotiations Underway from sponsor'
        
        db.session.commit()
        return jsonify({'message': 'Action taken successfully!'})
    

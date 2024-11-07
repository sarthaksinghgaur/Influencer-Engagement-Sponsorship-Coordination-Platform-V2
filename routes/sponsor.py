from flask import jsonify, session, request
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted
from models import *

class SponsorDashboard(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def get(self):
        user = User.query.get(session['user_id'])
        if not user or user.role != 'sponsor':
            return jsonify({'message': 'You do not have permission to access the sponsor dashboard.'}), 403

        sponsor = Sponsor.query.filter_by(user_id=user.id).first()
        if not sponsor:
            return jsonify({'message': 'Please complete your sponsor registration.'}), 400

        campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
        ad_requests = AdRequest.query.filter_by(sponsor_id=sponsor.id).all()

        return jsonify({
            'user': {'id': user.id, 'username': user.username, 'role': user.role},
            'sponsor': {'id': sponsor.id, 'company_name': sponsor.company_name},
            'campaigns': [{'id': campaign.id, 'name': campaign.name} for campaign in campaigns],
            'ad_requests': [{'id': ad_request.id, 'status': ad_request.status} for ad_request in ad_requests]
        })
    
class CreateCampaign(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def get(self):
        return jsonify({'message': 'Render the campaign creation form here.'})

    @auth_token_required
    @roles_accepted('sponsor')
    def post(self):
        user = User.query.get(session['user_id'])
        if not user or user.role != 'sponsor':
            return jsonify({'message': 'You do not have permission to create a campaign.'}), 403

        name = request.form['name']
        description = request.form['description']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        budget = request.form['budget']
        visibility = request.form['visibility']
        goals = request.form['goals']
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
        campaign.name = request.form['name']
        campaign.description = request.form['description']
        campaign.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        campaign.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        campaign.budget = request.form['budget']
        campaign.visibility = request.form['visibility']
        campaign.goals = request.form['goals']

        db.session.commit()
        return jsonify({'message': 'Campaign updated successfully!'})
    

class DeleteCampaign(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def delete(self, campaign_id):
        user = User.query.get(session['user_id'])
        if not user or user.role != 'sponsor':
            return jsonify({'message': 'You do not have permission to delete this campaign.'}), 403

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
        user = User.query.get(session['user_id'])
        sponsor = Sponsor.query.filter_by(user_id=user.id).first()
        campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
        influencers = Influencer.query.all()
        return jsonify({
            'campaigns': [{'id': campaign.id, 'name': campaign.name} for campaign in campaigns],
            'influencers': [{'id': influencer.id, 'name': influencer.name} for influencer in influencers]
        })

    @auth_token_required
    @roles_accepted('sponsor')
    def post(self):
        user = User.query.get(session['user_id'])
        if not user or user.role != 'sponsor':
            return jsonify({'message': 'You do not have permission to create an ad request.'}), 403

        name = request.form['name']
        sponsor = Sponsor.query.filter_by(user_id=user.id).first()
        sponsor_id = sponsor.id
        campaign_id = request.form['campaign_id']
        messages = request.form['messages']
        requirements = request.form['requirements']
        payment_amount = request.form['payment_amount']
        status = "Available"

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
        influencers = User.query.filter_by(role='influencer').all()
        ad_request_data = {
            'id': ad_request.id,
            'name': ad_request.name,
            'messages': ad_request.messages,
            'requirements': ad_request.requirements,
            'payment_amount': ad_request.payment_amount,
            'status': ad_request.status,
            'campaigns': [{'id': campaign.id, 'name': campaign.name} for campaign in campaigns],
            'influencers': [{'id': influencer.id, 'name': influencer.username} for influencer in influencers]
        }
        return jsonify(ad_request_data)

    @auth_token_required
    @roles_accepted('sponsor')
    def post(self, ad_request_id):
        ad_request = AdRequest.query.get_or_404(ad_request_id)
        ad_request.name = request.form['name']
        ad_request.messages = request.form['messages']
        ad_request.requirements = request.form['requirements']
        ad_request.payment_amount = request.form['payment_amount']
        ad_request.status = request.form['status']
        
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
    

from flask_restful import Resource
from flask import jsonify, make_response, request, session
from flask_security import login_user, verify_password, logout_user
from flask_security.utils import hash_password
from flask_security import auth_token_required, roles_accepted
from models import db, user_datastore, Sponsor, Influencer
from flask_login import current_user

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username:
            return make_response(jsonify({"message": "Username is required"}), 400)
        if not password:
            return make_response(jsonify({"message": "Password is required"}), 400)
        
        user = user_datastore.find_user(username=username)
        if user:
            if verify_password(password, user.password):
                if user.active: 
                    token = user.get_auth_token()
                    if token:
                        login_user(user)
                        db.session.commit()

                        if user.roles[0].name == 'admin': 
                            is_complete = True
                        
                        elif user.roles[0].name == 'influencer':
                            influencer = Influencer.query.filter_by(user_id=user.id).first()
                            if influencer:
                                is_complete = True
                                if influencer.flagged:
                                    return make_response(jsonify({"message": "Your account has been flagged."}), 403)
                            else:
                                is_complete = False                        
                        
                        elif user.roles[0].name == 'sponsor':
                            sponsor = Sponsor.query.filter_by(user_id=user.id).first()
                            if sponsor:
                                is_complete = True
                                if sponsor.flagged:
                                    return make_response(jsonify({"message": "Your account has been flagged."}), 403) 
                                if not sponsor.is_approved:
                                    return make_response(jsonify({"message": "Your account is pending approval."}), 403)
                            else:
                                is_complete = False  

                        return make_response(jsonify({"message": "Login successful", "authToken": token, "username": user.username, "role": user.roles[0].name, "id": user.id, "is_complete": is_complete}), 200)
                    else:
                        return make_response(jsonify({"message": "Unable to generate auth token"}), 500)
                else:
                    return make_response(jsonify({"message": "User account is inactive. Contact Admin."}), 403)
            else:
                return make_response(jsonify({"message": "Invalid password"}), 401)
        return make_response(jsonify({"message": "User not found", "username": username}), 404)


class Logout(Resource):
    def get(self):
        if current_user.is_authenticated:
            logout_user()
            session.clear()
            return make_response(jsonify({'message': 'You have been logged out successfully.'}), 200)
        else:
            return make_response(jsonify({'message': 'No active session found, but you have been logged out.'}), 200)   


class Signup(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        role = data.get('role')
        
        # Validation checks with improved consistency
        if not email:
            return make_response(jsonify({"message": "Email is required"}), 400)
        if not password:
            return make_response(jsonify({"message": "Password is required"}), 400)
        if not username:
            return make_response(jsonify({"message": "Username is required"}), 400)
        if not role:
            return make_response(jsonify({"message": "Role is required"}), 400)
        
        if user_datastore.find_user(email=email):
            return make_response(jsonify({"message": "User already exists", "email": email}), 409)

        hashed_password = hash_password(password)

        if role == 'influencer':
            influencer = user_datastore.create_user(email=email, password=hashed_password, username=username)
            user_datastore.add_role_to_user(influencer, "influencer")
            db.session.commit()

            user = user_datastore.find_user(username=username)
            token = user.get_auth_token()
            login_user(user)
            db.session.commit()

            return make_response(jsonify({"message": "User created", "id": influencer.id, "email": influencer.email, "authToken": token}), 201)

        elif role == 'sponsor':
            sponsor = user_datastore.create_user(email=email, password=hashed_password, username=username)
            user_datastore.add_role_to_user(sponsor, "sponsor")
            db.session.commit()

            user = user_datastore.find_user(username=username)
            token = user.get_auth_token()
            login_user(user)
            db.session.commit()

            return make_response(jsonify({"message": "User created", "id": sponsor.id, "email": sponsor.email, "authToken": token}), 201)
        
        else:
            return make_response(jsonify({"message": "Invalid role specified"}), 400)


class SponsorRegistration(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def post(self):
        data = request.get_json()
        company_name = data.get('company_name')
        industry = data.get('industry')
        budget = data.get('budget')

        if not company_name:
            return make_response(jsonify({"message": "Company name is required"}), 400)
        if not industry:
            return make_response(jsonify({"message": "Industry is required"}), 400)
        if not budget:
            return make_response(jsonify({"message": "Budget is required"}), 400)
        
        user = current_user

        sponsor = Sponsor(company_name=company_name, industry=industry, budget=budget, user=user, is_approved=False)
        db.session.add(sponsor)
        db.session.commit()

        return make_response(jsonify({"message": "Sponsor registration successful", "sponsor_id": sponsor.id}), 201)


class InfluencerRegistration(Resource):
    @auth_token_required
    @roles_accepted('influencer')
    def post(self):
        data = request.get_json()
        name = data.get('name')
        category = data.get('category')
        niche = data.get('niche')
        reach = data.get('reach')
        platform = data.get('platform')

        if not name:
            return make_response(jsonify({"message": "Name is required"}), 400)
        if not category:
            return make_response(jsonify({"message": "Category is required"}), 400)
        if not niche:
            return make_response(jsonify({"message": "Niche is required"}), 400)
        if not reach:
            return make_response(jsonify({"message": "Reach is required"}), 400)
        if not platform:
            return make_response(jsonify({"message": "Platform is required"}), 400)
        
        user = current_user

        influencer = Influencer(name=name, category=category, niche=niche, reach=reach, platform=platform, user=user)
        db.session.add(influencer)
        db.session.commit()

        return make_response(jsonify({"message": "Influencer registration successful", "influencer_id": influencer.id}), 201)

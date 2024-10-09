from flask_security import UserMixin, RoleMixin, AsaList, SQLAlchemyUserDatastore
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                    String, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    
    influencer = db.relationship('Influencer', uselist=False, back_populates='user', cascade="all, delete-orphan")
    sponsor = db.relationship('Sponsor', uselist=False, back_populates='user', cascade="all, delete-orphan")
    
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'last_login_at': self.last_login_at,
            'current_login_at': self.current_login_at,
            'last_login_ip': self.last_login_ip,
            'current_login_ip': self.current_login_ip,
            'login_count': self.login_count,
            'active': self.active,
            'fs_uniquifier': self.fs_uniquifier,
            'confirmed_at': self.confirmed_at
        }
    def get_all_users():
        return User.query.all()

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

class Influencer(db.Model):
    __tablename__ = 'influencer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    niche = db.Column(db.String(120), nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.String(120), nullable=False)
    flagged = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    user = db.relationship('User', back_populates='influencer')
    ad_requests = db.relationship('AdRequest', back_populates='influencer')

    def __repr__(self):
        return f'<Influencer {self.id} - {self.name}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'niche': self.niche,
            'reach': self.reach,
            'platform': self.platform,
            'flagged': self.flagged,
            'user_id': self.user_id
        }

    def get_all_influencers():
        return Influencer.query.all()
    
    def get_influencer_by_id(influencer_id):
        return Influencer.query.get(influencer_id)

    def get_influencer_by_name(influencer_name):
        return Influencer.query.filter_by(name=influencer_name).first()
    
    def get_influencer_by_user_id(user_id):
        return Influencer.query.filter_by(user_id=user_id).first()
    
    def get_flagged_influencers():
        return Influencer.query.filter_by(flagged=True).all()
    
    def get_unflagged_influencers():
        return Influencer.query.filter_by(flagged=False).all()
    
    def edit_influencer(influencer_id, name, category, niche, reach, platform):
        Influencer.query.filter_by(id=influencer_id).update({
            'name': name,
            'category': category,
            'niche': niche,
            'reach': reach,
            'platform': platform
        })
        db.session.commit()

    def delete_influencer(influencer_id):
        Influencer.query.filter_by(id=influencer_id).delete()
        db.session.commit()

    def flag_influencer(influencer_id):
        Influencer.query.filter_by(id=influencer_id).update({
            'flagged': True
        })
        db.session.commit()

    def unflag_influencer(influencer_id):
        Influencer.query.filter_by(id=influencer_id).update({
            'flagged': False
        })
        db.session.commit()
    


class Sponsor(db.Model):
    __tablename__ = 'sponsor'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120), nullable=False)
    industry = db.Column(db.String(120), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    flagged = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User', back_populates='sponsor')
    campaigns = db.relationship('Campaign', back_populates='sponsor')
    ad_requests = db.relationship('AdRequest', back_populates='sponsor')

    def __repr__(self):
        return f'<Sponsor {self.id} - {self.company_name}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'industry': self.industry,
            'budget': self.budget,
            'flagged': self.flagged,
            'user_id': self.user_id
        }

    def get_all_sponsors():
        return Sponsor.query.all()

    def get_sponsor_by_id(sponsor_id):
        return Sponsor.query.get(sponsor_id)
    
    def get_flagged_sponsors():
        return Sponsor.query.filter_by(flagged=True).all()
    
    def get_unflagged_sponsors():
        return Sponsor.query.filter_by(flagged=False).all()
    
    def edit_sponsor(sponsor_id, company_name, industry, budget):
        Sponsor.query.filter_by(id=sponsor_id).update({
            'company_name': company_name,
            'industry': industry,
            'budget': budget
        })
        db.session.commit()

    def delete_sponsor(sponsor_id):
        Sponsor.query.filter_by(id=sponsor_id).delete()
        db.session.commit()

    def flag_sponsor(sponsor_id):
        Sponsor.query.filter_by(id=sponsor_id).update({
            'flagged': True
        })
        db.session.commit()

    def unflag_sponsor(sponsor_id):
        Sponsor.query.filter_by(id=sponsor_id).update({
            'flagged': False
        })
        db.session.commit()

    


class Campaign(db.Model):
    __tablename__ = 'campaign'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.String(10), nullable=False)  # 'public' or 'private'
    flagged = db.Column(db.Boolean, default=False)
    goals = db.Column(db.Text, nullable=False)
    
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)

    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True, cascade='all, delete-orphan')
    sponsor = db.relationship('Sponsor', back_populates='campaigns')

    def __repr__(self):
        return f'<Campaign {self.id} - {self.name} - {self.visibility}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'budget': self.budget,
            'visibility': self.visibility,
            'goals': self.goals,
            'sponsor_id': self.sponsor_id
        }

    def get_all_campaigns():
        return Campaign.query.all()

    def get_campaign_by_id(campaign_id):
        return Campaign.query.get(campaign_id)

    def get_flagged_campaigns():
        return Campaign.query.filter_by(flagged=True).all()
    
    def get_unflagged_campaigns():
        return Campaign.query.filter_by(flagged=False).all()
    
    def edit_campaign(campaign_id, name, description, start_date, end_date, budget, visibility, goals):
        Campaign.query.filter_by(id=campaign_id).update({
            'name': name,
            'description': description,
            'start_date': start_date,
            'end_date': end_date,
            'budget': budget,
            'visibility': visibility,
            'goals': goals
        })
        db.session.commit()

    def delete_campaign(campaign_id):
        Campaign.query.filter_by(id=campaign_id).delete()
        db.session.commit()

    def flag_campaign(campaign_id):
        Campaign.query.filter_by(id=campaign_id).update({
            'flagged': True
        })
        db.session.commit()

    def unflag_campaign(campaign_id):
        Campaign.query.filter_by(id=campaign_id).update({
            'flagged': False
        })
        db.session.commit()


class AdRequest(db.Model):
    __tablename__ = 'ad_request'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    messages = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False) 

    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=True)

    influencer = db.relationship('Influencer', back_populates='ad_requests')
    sponsor = db.relationship('Sponsor', back_populates='ad_requests')

    def __repr__(self):
        return f'<AdRequest {self.id} - {self.name} - {self.status}>'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'messages': self.messages,
            'requirements': self.requirements,
            'payment_amount': self.payment_amount,
            'status': self.status,
            'sponsor_id': self.sponsor_id,
            'campaign_id': self.campaign_id,
            'influencer_id': self.influencer_id
        }

    def get_all_ad_requests():
        return AdRequest.query.all()

    def get_ad_request_by_id(ad_request_id):
        return AdRequest.query.get(ad_request_id)
    
    def edit_ad_request(ad_request_id, name, messages, requirements, payment_amount, status):
        AdRequest.query.filter_by(id=ad_request_id).update({
            'name': name,
            'messages': messages,
            'requirements': requirements,
            'payment_amount': payment_amount,
            'status': status
        })
        db.session.commit()

    def delete_ad_request(ad_request_id):
        AdRequest.query.filter_by(id=ad_request_id).delete()
        db.session.commit()

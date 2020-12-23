'''
Database Model
'''

from dataclasses import dataclass
from datetime import datetime

import jwt
import pytz

from flask_login import UserMixin

from . import app, db


@dataclass
class Users(db.Model, UserMixin):
    '''Users Database Table'''
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id: int
    email: str
    password: str
    tz: str
    created: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(length=255), unique=True, nullable=False)
    password = db.Column(db.String(length=255), nullable=False)
    tz = db.Column(db.String(length=30), default='UTC')
    created = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.utc))

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            token_disabled = DisabledToken.check_disabled(auth_token)
    
            if token_disabled:
                return 'Token disabled. Please log in again.'

            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


@dataclass
class ApiKeys(db.Model):
    '''API Keys Database Table'''
    __tablename__ = 'api_keys'
    __table_args__ = {'extend_existing': True}

    id: int
    key: str
    user_id: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(length=36), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)


@dataclass
class PasswordReset(db.Model):
    '''Password Reset Database Table'''
    __tablename__ = 'password_reset'
    __table_args__ = {'extend_existing': True}

    id: int
    ref: str
    user_id: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ref = db.Column(db.String(length=36), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

@dataclass
class DisabledToken(db.Model):
    __tablename__ = 'disabled_tokens'
    __table_args__ = {'extend_existing': True}

    id: int
    token: str
    disabled_on: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    disabled_on = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.utc))

    @staticmethod
    def check_disabled(auth_token):
        return True if db.session.query(DisabledToken).filter_by(token=str(auth_token)).first() else False
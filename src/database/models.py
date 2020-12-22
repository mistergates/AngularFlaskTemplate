'''
Database Model
'''

from dataclasses import dataclass
from datetime import datetime

import pytz

from flask_login import UserMixin

from . import db


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

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(length=255), unique=True, nullable=False)
    password = db.Column(db.String(length=255), nullable=False)
    tz = db.Column(db.String(length=30), default='UTC')
    created = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.utc))


@dataclass
class ApiKeys(db.Model):
    '''API Keys Database Table'''
    __tablename__ = 'apiKeys'
    __table_args__ = {'extend_existing': True}

    id: int
    key: str
    user_id: str

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(length=36), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)


@dataclass
class PasswordReset(db.Model):
    '''Password Reset Database Table'''
    __tablename__ = 'passwordReset'
    __table_args__ = {'extend_existing': True}

    id: int
    ref: str
    user_id: str

    id = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.String(length=36), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

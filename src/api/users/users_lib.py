'''
Users API Library
'''
from uuid import uuid4

from flask import jsonify, abort, request
from flask_login import login_user, current_user, login_manager
from passlib.hash import sha256_crypt

from . import models, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.Users).filter_by(id=user_id).first()


def user_registration(payload):
    required_fields = ['password', 'email']

    if not payload:
        abort(400, 'Payload is empty.')

    if any(x not in payload.keys() for x in required_fields):
        abort(400, 'Missing required fields in payload.')

    if db.session.query(models.Users).filter_by(email=payload['email']).first():
        abort(400, description='User already exists with provided email address.')

    user = models.Users(
        password=_generate_hash(payload['password']),
        email=payload['email']
    )
    db.session.add(user)
    db.session.flush()

    # Create API key
    api_key = models.ApiKeys(
        key=str(uuid4()),
        user_id=user.id
    )
    db.session.add(api_key)
    db.session.commit()

    login_user(user, remember=payload.get('remember_me', False))
    return jsonify({'status': 'success'}), 201


def user_login(payload):
    required_fields = ['email', 'password']

    if not payload:
        print('empty payload')
        abort(400, 'Payload is empty.')

    if any(x not in payload.keys() for x in required_fields):
        abort(400, 'Missing required fields in payload.')

    user = db.session.query(models.Users).filter_by(email=payload['email']).first()
    if not user or not _verify_hash(payload['password'], user.password):
        abort(400, 'Invalid credentials.')

    # Generate JWT
    auth_token = user.encode_auth_token(user.id)

    # Set user as logged in
    login_user(user, remember=payload.get('remember_me', False))
    return jsonify({'status': 'success', 'message': 'Login successful.', 'auth_token': auth_token}), 200


def user_logout():
    auth_token = _get_auth_token(request.headers)
    if not auth_token:
        return jsonify({'status': 'error', 'message': 'Invalid authorizaiton token.'}), 401

    resp = models.Users.decode_auth_token(auth_token)

    if isinstance(resp, str):
        return jsonify({'status': 'error', 'message': resp}), 401

    disable_token = models.DisabledToken(token=auth_token)
    db.session.add(disable_token)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Logout successful.'})


def gen_api_key(payload):
    user = db.session.query(models.Users).filter_by(id=current_user.id).first()

    if not user:
        abort(401, 'Unauthorized')

    if not _verify_hash(payload['password'], user.password):
        abort(400, 'Invalid credentials.')

    api_key = db.session.query(models.ApiKeys).filter_by(user_id=current_user.id).first()
    api_key.key = str(uuid4())
    db.session.commit()

    return jsonify({'status': 'success', 'key': api_key.key}), 200


def get_api_key():
    api_key = db.session.query(models.ApiKeys).filter_by(user_id=current_user.id).first()
    return jsonify({'key': api_key.key}), 200


def get_timezone():
    user = db.session.query(models.Users).filter_by(id=current_user.id).first()
    return jsonify({'timezone': user.tz}), 200


def set_timezone(payload):
    user = db.session.query(models.Users).filter_by(id=current_user.id).first()
    user.tz = payload.get('timezone', user.tz)
    db.session.commit()

    return jsonify({'status': 'success'}), 200


# ---------------------------
# Internal Functions
# ---------------------------
def _generate_hash(password):
    return sha256_crypt.hash(password)


def _verify_hash(password, password_hash):
    return sha256_crypt.verify(password, password_hash)


def _get_user(email):
    user = db.session.query(models.Users).filter_by(email=email).first()
    return user._asdict() if user else None


def _verify_password(email, password):
    user = db.session.query(models.Users).filter_by(email=email).first()
    return _verify_hash(password, user.password)


def _get_auth_token(headers):
    auth_header = headers.get('Authorization', None)
    auth_token = auth_header.split(" ")[1] if auth_header else None
    return auth_token

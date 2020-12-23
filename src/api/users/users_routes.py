'''
Users API Routes
'''
from flask import Blueprint, request
from flask_login import login_required
from . import users_lib, app

ENDPOINT = 'users'
users_api = Blueprint('users_api', __name__)

# ------------------------------- #
# POST REQUESTS
# ------------------------------- #
@users_api.route(f'{app.config["API_BASE"]}/{ENDPOINT}/register', methods=['POST'])
def user_registration():
    print(request.get_json(force=True))
    return users_lib.user_registration(request.get_json(force=True))


@users_api.route(f'{app.config["API_BASE"]}/{ENDPOINT}/login', methods=['POST'])
def user_login():
    print(request.get_json(force=True))
    return users_lib.user_login(request.get_json(force=True))


@users_api.route(f'{app.config["API_BASE"]}/{ENDPOINT}/logout', methods=['POST'])
@login_required
def user_logout():
    return users_lib.user_logout()


@users_api.route(f'{app.config["API_BASE"]}/{ENDPOINT}/generateApiKey', methods=['POST'])
@login_required
def gen_api_key():
    print(request.get_json(force=True))
    return users_lib.gen_api_key(request.get_json(force=True))


# ------------------------------- #
# PATCH REQUESTS
# ------------------------------- #
@users_api.route(f'{app.config["API_BASE"]}/{ENDPOINT}/timezone', methods=['PATCH'])
@login_required
def set_timezone():
    return users_lib.set_timezone(request.get_json(force=True))


# ------------------------------- #
# GET REQUESTS
# ------------------------------- #
@users_api.route(f'{app.config["API_BASE"]}/{ENDPOINT}/api_key', methods=['GET'])
@login_required
def get_api_key():
    return users_lib.get_api_key()


@users_api.route(f'{app.config["API_BASE"]}/{ENDPOINT}/timezone', methods=['GET'])
@login_required
def get_timezone():
    return users_lib.get_timezone()

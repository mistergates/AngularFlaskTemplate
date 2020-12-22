'''
Flask API App
'''
import pytz

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

from . import NAME, API_BASE, config

# ---------------------------
# Configure Flask App
# ---------------------------
app = Flask(NAME)
app.config['SECRET_KEY'] = config['App']['secret']
app.config['SQLALCHEMY_DATABASE_URI'] = config['Database']['uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.getboolean('Database', 'track_modifications')
app.config['TIMEZONES'] = pytz.common_timezones
app.config['DEFAULT_TIMEZONE'] = 'UTC'
app.config['API_BASE'] = API_BASE

# ---------------------------
# Allow Cross-origin Reqs
# ---------------------------
CORS(app, supports_credentials=True)

# ---------------------------
# Initialize Database
# ---------------------------
db = SQLAlchemy(app)

# ---------------------------
# Initialize Login Manager
# ---------------------------
login_manager = LoginManager(app)

# ---------------------------
# Register Blueprints
# ---------------------------
from .users.users_routes import users_api
blueprints = [
    users_api
]
for bp in blueprints:
    app.register_blueprint(bp)

# ---------------------------
# Error Handlers
# ---------------------------
@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

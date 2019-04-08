from flask import Flask, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

from config import Config
from log import config_logger

config_logger()

app = Flask(__name__)

app.secret_key = Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import *
from routes.user import user_api
from routes.home import home_api
from helper.encoder import CustomJSONEncoder

app.register_blueprint(user_api)
app.register_blueprint(home_api)
app.json_encoder = CustomJSONEncoder


@app.before_request
def session_filter():
    if 'logged_in' not in session and request.endpoint not in ['user_api.login', 'user_api.join']:
        return redirect(url_for('user_api.login'))

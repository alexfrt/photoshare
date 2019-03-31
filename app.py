from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from config import Config
from log import config_logger

config_logger()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import *
from routes.user import user_api

app.register_blueprint(user_api)


@app.route("/")
def root():
    return redirect(url_for('login_api.login'))

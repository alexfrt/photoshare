from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)

app.register_blueprint(login_api)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

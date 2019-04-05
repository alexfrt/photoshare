import logging

from flask import Blueprint, redirect, url_for, render_template, request, session

from config import Config
from services.photo import get_last_photos, save_photo
from services.user import find_user

home_api = Blueprint('home_api', __name__)
logger = logging.getLogger(__name__)

photos = []
users = []


@home_api.route("/")
def home():
    if 'user' not in session:
        return redirect(url_for('user_api.login'))

    photos = get_last_photos()

    if photos:
        photos = photos[1:]
        photos[0]['active'] = 'active'

    return render_template('home.html', photos=photos, bucket=Config.S3_BUCKET_NAME, users=users)


@home_api.route("/upload", methods=['POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('user_api.login'))

    if 'photo' not in request.files or request.files['photo'].filename == '':
        return redirect(url_for('home_api.home'))

    save_photo(session['user'], request.files['photo'].stream, request.form['description'])

    return redirect(url_for("home_api.home"))

@home_api.route("/search", methods=['GET', 'POST'])
def search():
    if 'user' not in session:
        return redirect(url_for('user_api.login'))

    users = find_user(request.form['nick'])

    return render_template('home.html', photos=photos, bucket=Config.S3_BUCKET_NAME, users=users)

import logging

from flask import Blueprint, redirect, url_for, render_template, request, session

from config import Config
from services.photo import get_last_photos, save_photo, like_photo, dislike_photo
from services.user import find_user

home_api = Blueprint('home_api', __name__)
logger = logging.getLogger(__name__)


@home_api.route("/")
def home():
    photos = get_last_photos(session['user'])
    if len(photos) > 0:
        photos[0]['active'] = 'active'

    return render_template('home.html', photos=photos, bucket=Config.S3_BUCKET_NAME, users=[])


@home_api.route("/search", methods=['GET', 'POST'])
def search():
    users = find_user(request.form['nick'])
    photos = get_last_photos(session['user'])
    if len(photos) > 0:
        photos[0]['active'] = 'active'

    return render_template('home.html', photos=photos, bucket=Config.S3_BUCKET_NAME, users=users)


@home_api.route("/like/<photo_uuid>", methods=['GET'])
def like(photo_uuid):
    like_photo(photo_uuid, session['user'])
    return redirect(url_for("home_api.home"))


@home_api.route("/dislike/<photo_uuid>", methods=['GET'])
def dislike(photo_uuid):
    dislike_photo(photo_uuid, session['user'])
    return redirect(url_for("home_api.home"))


@home_api.route("/upload", methods=['POST'])
def upload():
    if 'photo' not in request.files or request.files['photo'].filename == '':
        return redirect(url_for('home_api.home'))

    save_photo(session['user'], request.files['photo'].stream, request.form['description'])

    return redirect(url_for("home_api.home"))

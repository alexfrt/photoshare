import logging
from datetime import datetime
from time import strptime, mktime

from flask import Blueprint, redirect, url_for, render_template, request, session, flash

from config import Config
from routes import messages
from services.photo import get_last_photos, save_photo, like_photo, dislike_photo
from services.user import find_user

home_api = Blueprint('home_api', __name__)
logger = logging.getLogger(__name__)


@home_api.route("/")
def home():
    photos = get_last_photos(session['user'])
    return render_template('home.html', photos=photos, bucket=Config.S3_BUCKET_NAME, users=[])


@home_api.route("/search", methods=['GET', 'POST'])
def search():
    users = find_user(request.form['nick'])
    photos = get_last_photos(session['user'])
    return render_template('home.html', photos=photos, bucket=Config.S3_BUCKET_NAME, users=users)


@home_api.route("/filter", methods=['POST'])
def date_filter():
    start = datetime.fromtimestamp(mktime(strptime(request.form['start'], "%d/%m/%Y")))
    end = datetime.fromtimestamp(mktime(strptime(request.form['end'], "%d/%m/%Y")))

    if start < end:
        photos = get_last_photos(session['user'], start, end)
        return render_template('home.html', photos=photos, bucket=Config.S3_BUCKET_NAME)
    else:
        flash(messages.INVALID_DATE_FILTER)
        return redirect(url_for("home_api.home"))


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

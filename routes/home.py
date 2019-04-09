from datetime import datetime
from time import strptime, mktime

from flask import Blueprint, redirect, url_for, render_template, request, session, flash

from config import Config
from routes import messages
from services.photo import get_last_photos, save_photo, like_photo, dislike_photo, get_photo_by_user
from services.user import get_users, find_by_nick

home_api = Blueprint('home_api', __name__)


@home_api.route("/")
def home():
    photos = get_last_photos(session['user']['nick'])
    users = get_users()
    return render_template('home.html', photos=photos, bucket=Config.S3_BUCKET_NAME, error=None, users=users)


@home_api.route("/user/<nick>", methods=['GET'])
def find_user(nick):
    u = find_by_nick(nick)
    photos = get_photo_by_user(u.nick)
    users = get_users()
    return render_template('home.html', photos=photos, bucket=Config.S3_BUCKET_NAME, error=None, visited_user=u)


@home_api.route("/filter", methods=['POST'])
def date_filter():
    start = datetime.fromtimestamp(mktime(strptime(request.form['start'], "%d/%m/%Y")))
    end = datetime.fromtimestamp(mktime(strptime(request.form['end'], "%d/%m/%Y")))

    if start < end:
        photos = get_last_photos(session['user']['nick'], start, end)
        users = get_users()
        return render_template('home.html', photos=photos, bucket=Config.S3_BUCKET_NAME, error=None, users=users)
    else:
        flash(messages.INVALID_DATE_FILTER)
        return redirect(url_for("home_api.home"))


@home_api.route("/like/<photo_uuid>", methods=['GET'])
def like(photo_uuid):
    like_photo(photo_uuid, session['user']['nick'])
    return redirect(url_for("home_api.home"))


@home_api.route("/dislike/<photo_uuid>", methods=['GET'])
def dislike(photo_uuid):
    dislike_photo(photo_uuid, session['user']['nick'])
    return redirect(url_for("home_api.home"))


@home_api.route("/upload", methods=['POST'])
def upload():
    if 'photo' not in request.files or request.files['photo'].filename == '':
        return redirect(url_for('home_api.home'))

    save_photo(session['user']['nick'], request.files['photo'].stream, request.form['description'])
    return redirect(url_for("home_api.home"))

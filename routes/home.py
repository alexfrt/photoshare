from datetime import datetime, timedelta
from time import strptime, mktime

from flask import Blueprint, redirect, url_for, render_template, request, session, flash

from config import Config
from routes import messages
from services.photo import get_last_photos, save_photo, like_photo, dislike_photo, get_photo_by_user, process_likes
from services.user import get_users, find_by_nick

home_api = Blueprint('home_api', __name__)


@home_api.route("/")
def home():
    photos = get_last_photos()
    process_likes(session['user']['nick'], photos)
    users = get_users()
    return render_template('home.html', photos=photos, bucket=Config.CLOUD_STORAGE_BUCKET, error=None, users=users)


@home_api.route("/user/<nick>", methods=['GET'])
def find_user(nick):
    u = find_by_nick(nick)
    photos = get_photo_by_user(u.nick)
    process_likes(session['user']['nick'], photos)
    return render_template('home.html', photos=photos, bucket=Config.CLOUD_STORAGE_BUCKET, error=None, visited_user=u,
                           users=get_users())


@home_api.route("/filter", methods=['POST'])
def date_filter():
    start = datetime.fromtimestamp(mktime(strptime(request.form['start'], "%d/%m/%Y")))
    end = datetime.fromtimestamp(mktime(strptime(request.form['end'], "%d/%m/%Y"))) + timedelta(hours=23, minutes=59,
                                                                                                seconds=59)

    if start < end:
        photos = get_last_photos(start, end)
        process_likes(session['user']['nick'], photos)
        users = get_users()
        return render_template('home.html', photos=photos, bucket=Config.CLOUD_STORAGE_BUCKET, error=None, users=users)
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
    
    file = request.files.get('photo')

    save_photo(session['user']['nick'], file.read(), file.filename, request.form['description'])
    return redirect(url_for("home_api.home"))

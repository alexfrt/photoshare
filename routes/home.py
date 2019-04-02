import logging

from flask import Blueprint, redirect, url_for, render_template, request, session

from services.photo import get_last_photos, save_photo

home_api = Blueprint('home_api', __name__)
logger = logging.getLogger(__name__)


@home_api.route("/")
def home():
    if 'user' not in session:
        return redirect(url_for('user_api.login'))

    photos = get_last_photos()

    return render_template('home.html', photos=photos)


@home_api.route("/upload", methods=['POST'])
def upload():
    if 'photo' not in request.files:
        return redirect(url_for('home_api.home'))

    file = request.files['photo']
    save_photo(session['user'], file)

    return redirect(url_for("home_api.home"))

import logging

from flask import Blueprint, render_template, request, session, redirect, url_for

from helper.request import contains_required_params
from models.user import User
from routes import messages
from services.photo import get_last_photos
from services.user import check_user_credentials, InvalidCredentialsException, create_user, update_user

user_api = Blueprint('user_api', __name__)
logger = logging.getLogger(__name__)


@user_api.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        if not contains_required_params(['nick', 'password'], request.form):
            error = messages.MISSING_FORM_PARAM
        else:
            try:
                user = check_user_credentials(request.form['nick'], request.form['password'])
                session['user'] = user
                session['logged_in'] = True

                logger.info("user {} has logged in".format(user.nick))
                return redirect(url_for('home_api.home'))
            except InvalidCredentialsException as e:
                error = str(e)

    return render_template('login.html', error=error)


@user_api.route('/join', methods=['GET', 'POST'])
def join():
    error = None

    if request.method == 'POST':
        if not contains_required_params(['name', 'nick', 'password', 'email'], request.form):
            error = messages.MISSING_FORM_PARAM
        else:
            try:
                user = create_user(User(
                    request.form['name'],
                    request.form['nick'],
                    request.form['password'],
                    request.form['email']
                ))

                session['user'] = user
                session['logged_in'] = True

                logger.info("user {} has been created and logged in".format(user.nick))

                return redirect(url_for('home_api.home'))
            except Exception as e:
                error = str(e)

    return render_template('join.html', error=error)


@user_api.route('/settings', methods=['POST'])
def settings():
    error = None
    photo_profile = None
    pswd = None

    if request.method == 'POST':
        if not contains_required_params(['new_name', 'new_nick', 'new_email'], request.form):
            error = messages.MISSING_FORM_PARAM
        else:
            try:
                if request.form['new_password']:
                    pswd = request.form['new_password']

                if 'photo_profile' in request.files:
                    photo_profile =  request.files['photo_profile'].stream

                user = update_user(session["user"]["nick"], photo_profile,
                    User(
                        request.form['new_name'],
                        request.form['new_nick'],
                        pswd,
                        request.form['new_email']
                    ))

                session['user'] = user

                logger.info("user {} has been updated successfully.".format(user.nick))

                return redirect(url_for('home_api.home'))
            except Exception as e:
                error = str(e)
    photos = get_last_photos(session['user']['nick'])
    return render_template('home.html', photos=photos, error=error)

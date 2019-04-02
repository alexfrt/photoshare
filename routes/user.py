import logging

from flask import Blueprint, render_template, request, session, redirect, url_for

from helper.request import contains_required_params
from models.user import User
from routes import messages
from services.user import check_user_credentials, InvalidCredentialsException, create_user

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
                session['user'] = user.nick

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

                session['user'] = user.nick
                logger.info("user {} has been created and logged in".format(user.nick))

                return redirect(url_for('home_api.home'))
            except Exception as e:
                error = str(e)

    return render_template('join.html', error=error)

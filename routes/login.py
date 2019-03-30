import logging

from flask import Blueprint, render_template, request, session

from services.login import user_login, InvalidCredentialsException

login_api = Blueprint('login_api', __name__)
logger = logging.getLogger(__name__)


@login_api.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        if "nick" not in request.form or "password" not in request.form:
            error = "Please provide the nick and the password"
        else:
            try:
                user = user_login(request.form['nick'], request.form['password'])
                session['user'] = user

                logger.info("user {} has logged in".format(user.nick))
            except InvalidCredentialsException as e:
                error = str(e)

    return render_template('login.html', error=error)

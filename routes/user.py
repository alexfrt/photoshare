import logging

from flask import Blueprint, render_template, request, session

from services.user import check_user_credentials, InvalidCredentialsException

user_api = Blueprint('user_api', __name__)
logger = logging.getLogger(__name__)


@user_api.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        if "nick" not in request.form or "password" not in request.form:
            error = "Please provide the nick and the password"
        else:
            try:
                user = check_user_credentials(request.form['nick'], request.form['password'])
                session['user'] = user

                logger.info("user {} has logged in".format(user.nick))
            except InvalidCredentialsException as e:
                error = str(e)

    return render_template('login.html', error=error)

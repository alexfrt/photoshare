import hashlib

from models.user import User


def check_user_credentials(nick, password):
    user = User.query.filter_by(nick=nick).first()

    if user is None or salt_user_password(user, password) != user.password:
        raise InvalidCredentialsException("invalid credentials")

    return user


def salt_user_password(user, password=None):
    if password is None:
        password = user.password
    return hashlib.sha1("{}--{}".format(password, user.nick))


class InvalidCredentialsException(Exception):
    pass

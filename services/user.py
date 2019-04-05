import hashlib

from app import db
from models.user import User


def create_user(user):
    salted_password = salt_user_password(user)
    user.password = salted_password

    db.session.add(user)
    db.session.commit()

    return user


def check_user_credentials(nick, password):
    user = User.query.filter_by(nick=nick).first()

    if user is None or salt_user_password(user, password) != user.password:
        raise InvalidCredentialsException("Invalid Credentials")

    return user


def salt_user_password(user, password=None):
    if password is None:
        password = user.password
    return hashlib.sha1("{}--{}".format(password, user.nick).encode("UTF-8")).hexdigest()


def find_user(nick):
    if nick:
        return User.query.filter(User.nick.like("%" + nick + "%")).all()


class InvalidCredentialsException(Exception):
    pass

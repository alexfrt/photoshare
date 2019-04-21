import hashlib

from app import db
from models.user import User
from services.photo import save_photo_profile


def create_user(user):
    salted_password = salt_user_password(user)
    user.password = salted_password

    db.session.add(user)
    db.session.commit()

    return user


def update_user(current_user, photo_profile, filename, user):
    new_user = User.query.filter_by(nick=current_user).first()
    new_user.nick = user.nick
    new_user.name = user.name
    new_user.email = user.email
    new_user.photo_profile = save_photo_profile(photo_profile, filename) if photo_profile and filename else None
    new_user.password = salt_user_password(user) if user.password else new_user.password

    db.session.commit()

    return new_user


def check_user_credentials(nick, password):
    user = User.query.filter_by(nick=nick).first()

    if user is None or salt_user_password(user, password) != user.password:
        raise InvalidCredentialsException("Invalid Credentials")

    return user


def salt_user_password(user, password=None):
    if password is None:
        password = user.password
    return hashlib.sha1("{}--{}".format(password, user.nick).encode("UTF-8")).hexdigest()


def get_users():
    return User.query.all()

def find_by_nick(nick):
    return User.query.filter(User.nick == nick).first()


class InvalidCredentialsException(Exception):
    pass

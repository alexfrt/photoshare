from datetime import datetime
from uuid import uuid4

from app import db
from models.photo import Photo
from models.user import User


def get_last_photos(user, start=None, end=None):
    if start is not None and end is not None:
        photos = list(
            Photo.query.filter(Photo.user is not None and Photo.when.between(start, end)).order_by(Photo.when))
    else:
        # noinspection PyComparisonWithNone
        photos = list(Photo.query.filter(Photo.user != None).order_by(Photo.when))

    for photo in photos:
        for user_liked in photo.likes:
            if user_liked.nick == user:
                photo.did_like = True
                break

    return photos


def get_photo_by_user(user):
    photos = list(Photo.query.filter(Photo.user == user).order_by(Photo.when))

    for photo in photos:
        for like in photo.likes:
            if like.nick == user:
                photo.did_like = True
                break

    return photos


def save_photo(user, stream, description):
    photo = Photo(uuid4().hex, user, description, datetime.now(), stream.read())
    db.session.add(photo)
    db.session.commit()


def save_photo_profile(stream):
    key = uuid4().hex

    photo = Photo(key, None, None, datetime.now(), stream.read())
    db.session.add(photo)

    return key


def like_photo(photo_uuid, user):
    photo = Photo.query.filter(Photo.uuid == photo_uuid).first()
    user = User.query.filter(User.nick == user).first()
    photo.likes.append(user)
    db.session.commit()


def dislike_photo(photo_uuid, user):
    photo = Photo.query.filter(Photo.uuid == photo_uuid).first()
    user = User.query.filter(User.nick == user).first()
    photo.likes.remove(user)
    db.session.commit()


def fetch_photo_data(photo_uuid):
    photo = Photo.query.filter(Photo.uuid == photo_uuid).first()
    if photo is not None:
        return photo.data

from datetime import datetime
from uuid import uuid4

from dateutil.parser import parse
from google.cloud import storage
from google.cloud import datastore
from werkzeug import secure_filename

from config import Config


def get_last_photos(start=None, end=None):
    photos = _query()
    if start is not None and end is not None:
        photos = [photo for photo in photos if start <= parse(photo['when']) <= end]

    return photos


def get_photo_by_user(user):
    return _query(user)


def process_likes(user, photos):
    for photo in photos:
        if 'likes' in photo:
            photo['num_likes'] = len(photo['likes'])
            photo['did_like'] = user in photo['likes']
        else:
            photo['num_likes'] = 0


def save_photo(user, photo, filename, description):
    filename_formated = _save(photo, filename)

    ds_client = datastore.Client(Config.PROJECT_ID)

    entity = datastore.Entity(
        key=ds_client.key('Photo'),
        exclude_from_indexes=['description', 'likes'])

    data = {
        'uuid': uuid4().hex,
        'filename': filename_formated,
        'user': user,
        'description': description,
        'when': datetime.now().isoformat(),
        'likes': list()
    }

    entity.update(data)
    ds_client.put(entity)


def save_photo_profile(photo, filename):
    return _save(photo, filename)


def like_photo(photo_uuid, user):
    ds_client = datastore.Client(Config.PROJECT_ID)

    query = ds_client.query(kind='Photo')
    query.add_filter('uuid', '=', photo_uuid)

    query_iterator = query.fetch()
    page = next(query_iterator.pages)

    entities = list(map(from_datastore, page))
    if len(entities) == 0:
        return

    photo = entities[0]
    if user not in photo['likes']:
        photo['likes'].append(user)

    ds_client.put(photo)


def dislike_photo(photo_uuid, user):
    ds_client = datastore.Client(Config.PROJECT_ID)

    query = ds_client.query(kind='Photo')
    query.add_filter('uuid', '=', photo_uuid)

    query_iterator = query.fetch()
    page = next(query_iterator.pages)

    entities = list(map(from_datastore, page))
    if len(entities) == 0:
        return

    photo = entities[0]
    if user in photo['likes']:
        photo['likes'].remove(user)

    ds_client.put(photo)


def from_datastore(entity):
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()

    entity['id'] = entity.key.id

    return entity


def _safe_filename(filename):
    filename = secure_filename(filename)
    date = datetime.now().isoformat()
    basename, extension = filename.rsplit('.', 1)
    return "{0}-{1}.{2}".format(basename, date, extension)


def _save(photo, filename):
    storage_client = storage.Client(project=Config.PROJECT_ID)
    bucket = storage_client.bucket(Config.CLOUD_STORAGE_BUCKET)
    filename_formated = _safe_filename(filename)
    blob = bucket.blob(filename_formated)

    blob.upload_from_string(
        photo,
        content_type="image/jpeg")

    return filename_formated


def _query(user=None):
    ds_client = datastore.Client(Config.PROJECT_ID)

    query = ds_client.query(kind='Photo')

    if user:
        query.add_filter('user', '=', user)

    query_iterator = query.fetch()
    page = next(query_iterator.pages)

    entities = list(map(from_datastore, page))

    return sorted(entities, key=lambda x: x['when'], reverse=True)

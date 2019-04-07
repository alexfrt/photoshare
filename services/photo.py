from datetime import datetime
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Key
from dateutil.parser import parse

from config import Config


def get_last_photos(user, start=None, end=None):
    dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION_NAME)
    table = dynamodb.Table(Config.DYNAMO_DB_TABLE)

    photos = table.scan()['Items']  # obviously not efficient
    if start is not None and end is not None:
        photos = [photo for photo in photos if start <= parse(photo['when']) <= end]

    sorted(photos, key=lambda p: p['when'], reverse=True)

    for photo in photos:
        if 'likes' in photo:
            photo['num_likes'] = len(photo['likes'])
            photo['did_like'] = user in photo['likes']
        else:
            photo['num_likes'] = 0

    return photos


def save_photo(user, photo, description):
    key = uuid4().hex

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(Config.S3_BUCKET_NAME)
    bucket.put_object(Key=key, Body=photo, ContentType="image/jpeg")

    dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION_NAME)
    table = dynamodb.Table(Config.DYNAMO_DB_TABLE)
    table.put_item(Item={
        'uuid': key,
        'user': user,
        'description': description,
        'when': datetime.now().isoformat(),
        'likes': list()
    })


def like_photo(photo_uuid, user):
    dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION_NAME)
    table = dynamodb.Table(Config.DYNAMO_DB_TABLE)

    photo = table.query(KeyConditionExpression=Key('uuid').eq(photo_uuid))['Items']
    if len(photo) == 0:
        return

    photo = photo[0]

    if user not in photo['likes']:
        table.update_item(
            Key={
                'uuid': photo_uuid
            },
            UpdateExpression="SET likes = list_append(likes, :user)",
            ExpressionAttributeValues={":user": [user]},
        )


def dislike_photo(photo_uuid, user):
    dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION_NAME)
    table = dynamodb.Table(Config.DYNAMO_DB_TABLE)

    photo = table.query(KeyConditionExpression=Key('uuid').eq(photo_uuid))['Items']
    if len(photo) == 0:
        return

    photo = photo[0]

    if user in photo['likes']:
        # obviously not atomic...
        table.update_item(
            Key={
                'uuid': photo_uuid
            },
            UpdateExpression="REMOVE likes[%d]" % photo['likes'].index(user)
        )

from datetime import datetime
from uuid import uuid4

import boto3

from config import Config


def get_last_photos():
    dynamodb = boto3.resource('dynamodb', region_name=Config.AWS_REGION_NAME)
    table = dynamodb.Table(Config.DYNAMO_DB_TABLE)
    return table.scan()['Items']


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
        'likes': 0
    })

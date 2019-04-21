import os


class Config(object):
    DEBUG = "DEBUG" in os.environ
    HTTP_PORT = int(os.environ.get('PORT', 5000))
    SECRET_KEY = os.environ.get("SECRET_KEY", "unsafeKey")
    DATA_BACKEND = 'cloudsql'
    PROJECT_ID = 'photoshare-app'
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = 'photoshare'
    DATABASE_NAME = 'photoshare'
    DATABASE_CONNECTION_NAME = 'photoshare-app:us-central1:photoshare'
    LOCAL_SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}').format(
            user=DATABASE_USER, password=DATABASE_PASSWORD,
            database=DATABASE_NAME)
    # When running on App Engine a unix socket is used to connect to the cloudsql
    # instance.
    LIVE_SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://{user}:{password}@localhost/{database}'
        '?unix_socket=/cloudsql/{connection_name}').format(
            user=DATABASE_USER, password=DATABASE_PASSWORD,
            database=DATABASE_NAME, connection_name=DATABASE_CONNECTION_NAME)
    if os.environ.get('GAE_INSTANCE'):
        DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
    else:
        DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI
    CLOUD_STORAGE_BUCKET = 'photoshare123'
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
import os


class Config(object):
    DEBUG = "DEBUG" in os.environ
    HTTP_PORT = int(os.environ.get('PORT', 5000))
    SECRET_KEY = os.environ.get("SECRET_KEY", "unsafeKey")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    PROJECT_ID = os.environ.get("PROJECT_ID", "photoshare")
    CLOUD_STORAGE_BUCKET = os.environ.get("CLOUD_STORAGE_BUCKET", "photoshare")
    DATABASE_USER = os.environ.get("DATABASE_USER", "photoshare")
    DATABASE_PASSWORD = os.environ.get("DATABASE_USER", "photoshare")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "photoshare")
    DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
    DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:3306/{database}'.format(
        user=DATABASE_USER, password=DATABASE_PASSWORD,
        host=DATABASE_HOST, database=DATABASE_NAME)

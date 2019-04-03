import os


class Config(object):
    DEBUG = "DEBUG" in os.environ
    HTTP_PORT = int(os.environ.get('PORT', 5000))
    SECRET_KEY = os.environ.get("SECRET_KEY", "unsafeKey")
    DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "photoshare")
    DATABASE_USER = os.environ.get("DATABASE_USER", "photoshare")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "photoshare")
    DATABASE_URI = "postgresql://%s:%s@%s/%s" % (DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME)
    AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME", "us-east-1")
    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "photoshare123")
    DYNAMO_DB_TABLE = os.environ.get("DYNAMO_DB_TABLE", "photoshare")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Config class for the app"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(16)
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

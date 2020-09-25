import os


class DevelopmentConfig:
    # Flask
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.urandom(32)

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ekiuranaiBBS.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


Config = DevelopmentConfig

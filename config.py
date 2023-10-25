import os
#basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = True
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///groceries.db" 
    DEBUG = True

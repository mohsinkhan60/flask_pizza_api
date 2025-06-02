import os
from decouple import config

BASR_DIR = os.path.dirname(os.path.realpath(__file__))
class Config:
   SECRET_KEY = config('SECRET_KEY', 'secret')
   SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = config('DEBUG', cast=bool)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASR_DIR, 'db.sqlite3')

class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass

config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}
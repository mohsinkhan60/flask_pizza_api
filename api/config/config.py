import os
from decouple import config

class Config:
   SECRET_KEY = config('SECRET_KEY', 'secret')


class DevConfig(Config):
    DEBUG = config('DEBUG', default=True, cast=bool)
    SQLALCHEMY_DATABASE_URI = config('DEV_DATABASE_URL', 'sqlite:///dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass

config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}
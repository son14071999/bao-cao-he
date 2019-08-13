import os
os_env =os.environ


class Config(object):
    SECRET_KEY = 'he'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class App_Config(Config):

    DEBUG = True
    DEBUG_TB_ENABLED = True  # Disable Debug toolbar
    TEMPLATES_AUTO_RELOAD = True
    JWT_SECRET_KEY = '1234567a@@'
    MONGO_DBNAME = 'dhpg'
    MONGO_HOST = 'localhost'
    MONGO_AUTH_SOURCE = 'admin'
    MONGO_URI = 'mongodb://localhost:33017/Demo'
    MONGO_CONNECT = False
    CONNECT = False
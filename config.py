import os
import json


ROOT_DIR = os.path.dirname(__file__)
CONFIG_FILE = f'{ROOT_DIR}/config.json'
LOCAL_HOST = '127.0.0.1'

with open(CONFIG_FILE, mode='r') as f:
    DATA = json.load(f)


class JsonConfig:
    @staticmethod
    def get(key: str, default=None):
        return DATA.get(key, default)

    @staticmethod
    def set(key: str, value=None):
        DATA[key] = value

        with open(CONFIG_FILE, mode='w') as config:
            json.dump(DATA, config, indent=4)


class DBConfig:
    DB_USER_NAME = JsonConfig.get('DB_USER_NAME', '__api__')
    DB_USER_PWD = JsonConfig.get('DB_USER_PWD', '0000')
    DB_HOST = JsonConfig.get('DB_HOST', LOCAL_HOST)
    DB_PORT = JsonConfig.get('DB_PORT', 27017)
    DB_NAME = JsonConfig.get('DB_NAME', 'test_db')
    DB_URI = f'mongodb://{DB_USER_NAME}:{DB_USER_PWD}@{DB_HOST}:{DB_PORT}'

    COL_ROUTES = 'routes'
    COL_ALARMS = 'alarms'
    COL_LOWEST = 'lowest'
    COL_TICKETS = 'tickets'


class APPConfig:
    ROOT_DIR = ROOT_DIR
    STATIC_DIR = f'{ROOT_DIR}/static'
    TEMPLATES_DIR = f'{ROOT_DIR}/templates'

    CONTROLLERS_MODULE_NAME = 'controllers'

    APP_MODE_PRODUCTION = 'production'
    APP_MODE_DEVELOPMENT = 'development'
    APP_MODE_TESTING = 'testing'

    APP_MODE = JsonConfig.get('APP_MODE', APP_MODE_PRODUCTION)
    APP_HOST = JsonConfig.get('APP_HOST', LOCAL_HOST)
    APP_PORT = JsonConfig.get('APP_PORT', 5000)

    @staticmethod
    def from_app_mode():
        return {
            APPConfig.APP_MODE_PRODUCTION: 'config.ProductionConfig',
            APPConfig.APP_MODE_DEVELOPMENT: 'config.DevelopmentConfig',
            APPConfig.APP_MODE_TESTING: 'config.TestingConfig'
        }.get(APPConfig.APP_MODE, 'config.ProductionConfig')


class FlaskConfig:
    SECRET_KEY = JsonConfig.get('PRODUCTION_SECRET_KEY', 'a1b51d8e3s21v6e5')
    SQLALCHEMY_DATABASE_URI = DBConfig.DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class ProductionConfig(FlaskConfig):
    ...


class DevelopmentConfig(FlaskConfig):
    SECRET_KEY = JsonConfig.get('DEVELOPMENT_SECRET_KEY', 'e1f8c3v1ew62d1dq')
    SQLALCHEMY_ECHO = True
    DEBUG = True
    TESTING = True


class TestingConfig(FlaskConfig):
    SECRET_KEY = JsonConfig.get('TESTING_SECRET_KEY', 'fe53s58ee3s2f5e3')
    TESTING = True


if __name__ == '__main__':
    ...


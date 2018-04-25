import os

BASE = os.path.abspath(os.path.dirname(__file__))
VAGRANT_IP = '192.168.10.11'

class Config(object):
    BASE_DIR = BASE
    DB_BASE_URI = 'mysql+pymysql://{}:{}@{}:{}/'.format(
        os.getenv('MYSQL_USER', 'root'),
        os.getenv('MYSQL_PASSWORD', 'root'),
        os.getenv('MYSQL_HOST', VAGRANT_IP),
        os.getenv('MYSQL_PORT', '3306')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_AUDIENCE = 'api audience'
    ISSUER = 'issuer'
    REDIS_HOST = os.getenv('REDIS_HOST', VAGRANT_IP)
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

class DevConfig(Config):
    DB_NAME = os.getenv('DB_NAME', 'benwaonline')
    SQLALCHEMY_DATABASE_URI = Config.DB_BASE_URI + DB_NAME
    DEBUG = True
    AUTH_URL = 'http://127.0.0.1:5002'
    JWKS_URL = AUTH_URL + '/.well-known/jwks.json'

class TestConfig(Config):
    DB_NAME = os.getenv('DB_NAME', 'benwaonlineapi_test')
    SQLALCHEMY_DATABASE_URI = Config.DB_BASE_URI + DB_NAME
    AUTH_URL = 'mock://mock'
    JWKS_URL = AUTH_URL + '/.well-known/jwks.json'
    TESTING = True
    WTF_CSRF_ENABLED = False

class ProdConfig(Config):
    DB_BASE_URI = 'mysql+pymysql://{}:{}@{}:{}/'.format(
        os.getenv('MYSQL_USER'),
        os.getenv('MYSQL_PASSWORD'),
        os.getenv('MYSQL_HOST'),
        os.getenv('MYSQL_PORT')
    )
    DB_NAME = os.getenv('DB_NAME', 'benwaonline')
    SQLALCHEMY_DATABASE_URI = DB_BASE_URI + DB_NAME
    DEBUG = False
    ISSUER = 'https://benwa.online'
    API_AUDIENCE = 'https://benwa.online/api'
    AUTH_URL = '{}:{}'.format(os.getenv('AUTH_URL'), os.getenv('AUTH_PORT'))
    JWKS_URL = AUTH_URL + '/.well-known/jwks.json'
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 666))

app_config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}

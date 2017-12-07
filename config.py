import os

BASE = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    BASE_DIR = BASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'not-so-secret'
    SECURITY_PASSWORD_SALT = 'super-secret'

    API_AUDIENCE = 'https://api.benwa.online'
    AUTH0_DOMAIN = 'choosegoose.auth0.com'
    AUTH0_CONSUMER_KEY = ''
    AUTH0_CONSUMER_SECRET = ''
    JWKS_URL = 'https://' + AUTH0_DOMAIN + '/.well-known/jwks.json'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/benwaonline'
    DEBUG = True
    SECRET_KEY = 'not-so-secret'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE, 'benwaonline_test.db')
    TESTING = True
    WTF_CSRF_ENABLED = False

class ProdConfig(Config):
    DEBUG = False
    SECRET_KEY = ''
    SECURITY_PASSWORD_SALT = ''

app_config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}

import os

BASE = os.path.abspath(os.path.dirname(__file__))

def get_secret(secret_name):
    '''Returns value provided by a docker secret, otherwise returns env'''
    try:
        with open('/run/secrets/' + secret_name, 'r') as f:
            data = f.read()
            return data.strip()
    except OSError:
        return os.getenv(secret_name)

class Config(object):
    BASE_DIR = BASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_AUDIENCE = 'api audience'
    ISSUER = 'issuer'
    MEMCACHED_HOST = os.getenv('MEMCACHED_HOST', '192.168.99.100')
    MEMCACHED_PORT = int(os.getenv('MEMCACHED_PORT', 11211))

class DevConfig(Config):
    DB_BASE_URI = 'mysql+pymysql://{}:{}@{}:{}/'.format(
        os.getenv('MYSQL_USER', 'root'),
        os.getenv('MYSQL_PASSWORD', ''),
        os.getenv('MYSQL_HOST', '127.0.0.1'),
        os.getenv('MYSQL_PORT', '3306')
    )
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = DB_BASE_URI + 'benwaonline'
    DEBUG = True
    AUTH_URL = 'http://127.0.0.1:5002'
    JWKS_URL = AUTH_URL + '/.well-known/jwks.json'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE, 'benwaonline_test.db')
    AUTH_URL = 'mock://mock'
    JWKS_URL = AUTH_URL + '/.well-known/jwks.json'
    TESTING = True
    WTF_CSRF_ENABLED = False

class ProdConfig(Config):
    DB_BASE_URI = 'mysql+pymysql://{}:{}@{}:{}/'.format(
        get_secret('MYSQL_USER'),
        get_secret('MYSQL_PASSWORD'),
        os.getenv('MYSQL_HOST'),
        os.getenv('MYSQL_PORT')
    )
    SQLALCHEMY_DATABASE_URI = DB_BASE_URI + 'benwaonline'
    DEBUG = False
    ISSUER = 'https://benwa.online'
    API_AUDIENCE = 'https://benwa.online/api'
    AUTH_URL = '{}:{}'.format(os.getenv('AUTH_URL'), os.getenv('AUTH_PORT'))
    JWKS_URL = AUTH_URL + '/.well-known/jwks.json'

app_config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}

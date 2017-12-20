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
    API_AUDIENCE = get_secret('API_AUDIENCE')
    AUTH0_DOMAIN = get_secret('AUTH0_DOMAIN')
    AUTH0_CONSUMER_KEY = ''
    AUTH0_CONSUMER_SECRET = ''
    JWKS_URL = 'https://' + AUTH0_DOMAIN + '/.well-known/jwks.json'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/benwaonline'
    DEBUG = True

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE, 'benwaonline_test.db')
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

app_config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}

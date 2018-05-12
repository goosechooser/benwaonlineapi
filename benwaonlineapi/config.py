import os

# BASE = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # BASE_DIR = BASE
    DB_BASE_URI = 'mysql+pymysql://{}:{}@{}:{}/'.format(
        os.getenv('MYSQL_USER'),
        os.getenv('MYSQL_PASSWORD'),
        os.getenv('MYSQL_HOST'),
        os.getenv('MYSQL_PORT')
    )
    DB_NAME = os.getenv('DB_NAME')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_AUDIENCE = 'api audience'
    ISSUER = 'issuer'
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    AUTH_URL = '{}:{}'.format(os.getenv('AUTH_URL'), os.getenv('AUTH_PORT', ''))
    JWKS_URL = AUTH_URL + '/.well-known/jwks.json'

class DevConfig(Config):
    # JWKS_URL = AUTH_URL + '/.well-known/jwks.json'
    pass

class TestConfig(Config):
    DB_NAME = 'benwaonlineapi_test'
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

    ISSUER = 'https://benwa.online'
    API_AUDIENCE = 'https://benwa.online/api'


app_config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig
}

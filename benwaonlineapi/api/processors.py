import requests
from jose import jwt

from flask import request, current_app
from flask_restless import ProcessingException
from flask_restless.views.base import catch_processing_exceptions

from benwaonlineapi.api.util import verify_token

AUTH0_DOMAIN = 'choosegoose.auth0.com'
ALGORITHMS = ['RS256']
ISSUER = 'https://' + AUTH0_DOMAIN + '/'
API_AUDIENCE = 'https://api.benwa.online'

# Should clean this up so it uses a reskinned ProcessingException
@catch_processing_exceptions
def get_token_header():
    auth = request.headers.get('authorization', None)
    if not auth:
        raise ProcessingException(title='authorization header missing',
                                    detail='authorization header is expected',
                                    status=401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise ProcessingException(title='invalid header',
                                    detail='authorization header must start with Bearer',
                                    status=401)
    elif len(parts) == 1:
        raise ProcessingException(title='invalid header',
                                    detail='token not found',
                                    status=401)
    elif len(parts) > 2:
        raise ProcessingException(title='invalid header',
                                    detail='authorization header must be Bearer token',
                                    status=401)
    token = parts[1]
    return token

def api_auth_func(data=None, **kw):
    token = get_token_header()
    # cache this
    jwksurl = requests.get('https://' + AUTH0_DOMAIN + '/.well-known/jwks.json')
    jwks = jwksurl.json()
    verified_token = verify_token(token, jwks)
    data['token'] = verified_token

def username_preproc(data=None, **kw):
    user_id = data['token']['sub'].split('|')[1]
    data['data']['attributes']['user_id'] = user_id

def remove_token(data=None, **kw):
    data.pop('token', None)

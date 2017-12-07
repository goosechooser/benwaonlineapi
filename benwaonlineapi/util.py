"""
Contains any utility functions used by processors or the benwaonline frontend.
"""
import requests
from jose import jwt
from flask import current_app
from flask_restless import ProcessingException
from flask_restless.views.base import catch_processing_exceptions

AUTH0_DOMAIN = 'choosegoose.auth0.com'
ALGORITHMS = ['RS256']
ISSUER = 'https://' + AUTH0_DOMAIN + '/'
API_AUDIENCE = 'https://api.benwa.online'

@catch_processing_exceptions
def verify_token(token, jwks, audience=API_AUDIENCE):
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=audience,
                issuer=ISSUER
            )
        except jwt.ExpiredSignatureError:
            raise ProcessingException(title='token expired',
                                    detail='token is expired',
                                    status=401)
        except jwt.JWTClaimsError:
            raise ProcessingException(title='invalid claim',
                                    detail='incorrect claims, check audience and issuer',
                                    status=401)
        except Exception:
            raise ProcessingException(title='invalid header',
                                    detail='unable to parse authentication token')
        return payload

    raise ProcessingException(title='invalid header', detail='unable to parse authentication token')

def get_jwks():
    jwksurl = requests.get(current_app.config['JWKS_URL'])
    jwks = jwksurl.json()
    return jwks

def requires_scope(required_scope, token):
    unverified_claims = jwt.get_unverified_claims(token)
    token_scopes = unverified_claims['scope'].split()
    return True if required_scope in token_scopes else False
"""
Contains any utility functions used by processors or the benwaonline frontend.
"""
import os
import requests
from jose import jwt, exceptions
from flask import current_app
from flask_restless import ProcessingException
from flask_restless.views.base import catch_processing_exceptions
from benwaonlineapi.config import app_config

cfg = app_config[os.getenv('FLASK_CONFIG')]
ALGORITHMS = ['RS256']

def verify_token(token, jwks, audience=cfg.API_AUDIENCE, issuer=cfg.ISSUER):
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
                issuer=issuer
            )
        except jwt.ExpiredSignatureError as err:
            raise ProcessingException(
                detail='{0}'.format(err),
                title='token expired',
                status=401
            )

        except jwt.JWTClaimsError as err:
            raise ProcessingException(
                detail='{0}'.format(err),
                title='invalid claim',
                status=401
            )

        except exceptions.JWTError as err:
            raise ProcessingException(
                detail='{0}'.format(err),
                title='invalid signature',
                status=401
            )

        except Exception as err:
            raise ProcessingException(title='invalid header',
                                    detail='unable to parse authentication token')

        return payload

    raise ProcessingException(title='invalid header', detail='unable to parse authentication token')

def get_jwks():
    try:
        jwksurl = requests.get(current_app.config['JWKS_URL'], timeout=5)
    except requests.exceptions.Timeout as err:
        raise ProcessingException(
            title='JWKS Request Timed Out',
            detail='the authentication server is unavailable, or another issue has occured',
            status=500
        )

    jwks = jwksurl.json()
    return jwks
def has_scope(scope, token):
    unverified_claims = jwt.get_unverified_claims(token)
    token_scopes = unverified_claims['scope'].split()
    return True if scope in token_scopes else False
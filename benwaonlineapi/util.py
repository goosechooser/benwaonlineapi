"""
Contains any utility functions used by processors or the benwaonline frontend.
"""
import os
import requests
from jose import jwt, exceptions
from flask import current_app
from flask_rest_jsonapi.exceptions import JsonApiException
from benwaonlineapi.config import app_config
from benwaonlineapi.cache import cache

cfg = app_config[os.getenv('FLASK_CONFIG')]
ALGORITHMS = ['RS256']

def verify_token(token):
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = match_key_id(unverified_header)

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=cfg.API_AUDIENCE,
            issuer=cfg.ISSUER
        )
    except jwt.ExpiredSignatureError as err:
        handle_expired_signature(unverified_header, err)
    except jwt.JWTClaimsError as err:
        handle_claims(err)
    except exceptions.JWTError as err:
        handle_jwt(err)
    except Exception:
        handle_non_jwt()
    return payload

def match_key_id(unverified_header):
    """Checks if the RSA key id given in the header exists in the JWKS."""
    jwks = get_jwks()
    rsa_keys = [
        rsa_from_jwks(key)
        for key in jwks["keys"]
        if key["kid"] == unverified_header["kid"]
    ]

    try:
        return rsa_keys[0]
    except IndexError:
        return None

def rsa_from_jwks(key):
    return {
        "kty": key["kty"],
        "kid": key["kid"],
        "use": key["use"],
        "n": key["n"],
        "e": key["e"]
    }

def handle_expired_signature(unverified_header, err):
    """Handles tokens with expired signatures."""
    msg = 'Token provided by {} has expired'.format(unverified_header.get('sub', 'sub not found'))
    current_app.logger.info(msg)
    raise JsonApiException(
        detail='{0}'.format(err),
        title='token expired',
        status=401
    )

def handle_claims(err):
    """Handles tokens with invalid claims."""
    raise JsonApiException(
        detail='{0}'.format(err),
        title='invalid claim',
        status=401
    )

def handle_jwt(err):
    """Handles tokens with other jwt-related issues."""
    raise JsonApiException(
        detail='{0}'.format(err),
        title='invalid signature',
        status=401
    )

def handle_non_jwt():
    """Handles everything else."""
    raise JsonApiException(title='invalid header',
                            detail='unable to parse authentication token')

def get_jwks():
    rv = cache.get('jwks')
    if rv is None:
        try:
            jwksurl = requests.get(current_app.config['JWKS_URL'], timeout=5)
        except requests.exceptions.Timeout:
            raise JsonApiException(
                title='JWKS Request Timed Out',
                detail='the authentication server is unavailable, or another issue has occured',
                status=500
        )
        rv = jwksurl.json()
        cache.set('jwks', rv, expire=48 * 3600)
    return rv

def has_scope(scope, token):
    unverified_claims = jwt.get_unverified_claims(token)
    token_scopes = unverified_claims['scope'].split()
    return True if scope in token_scopes else False

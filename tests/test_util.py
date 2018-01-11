from datetime import datetime, timedelta
import json

import pytest
from jose import jwt, exceptions
from flask_restless.views.base import ProcessingException
from flask import url_for

from benwaonlineapi import util
post_headers = {'Accept': 'application/vnd.api+json',
                'Content-Type': 'application/vnd.api+json'}

def get_pem(fname):
    with open(fname, 'r') as f:
        return f.read()

PRIV_KEY = get_pem('keys/benwaonline_api_test_priv.pem')
PUB_KEY = get_pem('keys/benwaonline_api_test_pub.pem')
ISSUER = 'issuer'
API_AUDIENCE = 'audience'

@pytest.fixture(scope='function')
def jwks():
    with open('keys/test_jwks.json', 'r') as f:
        JWKS = json.load(f)

    yield JWKS

def generate_jwt(claims):
    ''' Generates a JWT'''
    headers = {
        'typ': 'JWT',
        'alg': 'RS256',
        'kid': 'benwaonline_api_test'
    }
    return jwt.encode(claims, PRIV_KEY, algorithm='RS256', headers=headers)

def test_verify_token_invalid_signature(jwks):
    now = (datetime.utcnow() - datetime(1970, 1, 1))
    exp_at = now + timedelta(seconds=300)

    claims = {
        'iss': ISSUER,
        'aud': API_AUDIENCE,
        'sub': '6969',
        'iat': now.total_seconds(),
        'exp': exp_at.total_seconds()
    }
    token = generate_jwt(claims)

    jwks['keys'][0]['kid'] = 'invalid'
    with pytest.raises(ProcessingException):
        util.verify_token(token, jwks)

def test_verify_token_invalid_audience(jwks):
    claims = {
        'iss': ISSUER,
        'aud': 'invalid'
    }
    token = generate_jwt(claims)

    with pytest.raises(ProcessingException) as excinfo:
        util.verify_token(token, jwks)

def test_verify_token_invalid_issuer(jwks):
    claims = {
        'iss': 'invalid',
        'aud': API_AUDIENCE
    }
    token = generate_jwt(claims)
    with pytest.raises(ProcessingException):
        util.verify_token(token, jwks)

def test_verify_token_expired(jwks):
    now = (datetime(1971, 1, 1) - datetime(1970, 1, 1))
    exp_at = now + timedelta(seconds=300)

    claims = {
        'iss': ISSUER,
        'aud': API_AUDIENCE,
        'sub': '6969',
        'iat': now.total_seconds(),
        'exp': exp_at.total_seconds()
    }
    token = generate_jwt(claims)
    with pytest.raises(ProcessingException):
        util.verify_token(token, jwks)

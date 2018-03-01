import json
from datetime import datetime, timedelta

import pytest
from flask import url_for
from jose import exceptions, jwt

from benwaonlineapi import util
from flask_rest_jsonapi.exceptions import JsonApiException
from tests.helpers import generate_jwt

ISSUER = 'issuer'
API_AUDIENCE = 'audience'

def generate_jwt(claims, priv_key):
    ''' Generates a JWT'''
    headers = {
        'typ': 'JWT',
        'alg': 'RS256',
        'kid': 'benwaonline_api_test'
    }
    return jwt.encode(claims, priv_key, algorithm='RS256', headers=headers)

class TestVerifyToken(object):
    def test_invalid_signature(self, jwks, priv_key):
        now = (datetime.utcnow() - datetime(1970, 1, 1))
        exp_at = now + timedelta(seconds=300)

        claims = {
            'iss': ISSUER,
            'aud': API_AUDIENCE,
            'sub': '6969',
            'iat': now.total_seconds(),
            'exp': exp_at.total_seconds()
        }
        token = generate_jwt(claims, priv_key)

        jwks['keys'][0]['kid'] = 'invalid'
        with pytest.raises(JsonApiException):
            util.verify_token(token, jwks)

    def test_invalid_audience(self, jwks, priv_key):
        claims = {
            'iss': ISSUER,
            'aud': 'invalid'
        }
        token = generate_jwt(claims, priv_key)

        with pytest.raises(JsonApiException):
            util.verify_token(token, jwks)

    def test_invalid_issuer(self, jwks, priv_key):
        claims = {
            'iss': 'invalid',
            'aud': API_AUDIENCE
        }
        token = generate_jwt(claims, priv_key)
        with pytest.raises(JsonApiException):
            util.verify_token(token, jwks)

    def test_token_expired(self, jwks, priv_key):
        now = (datetime(1971, 1, 1) - datetime(1970, 1, 1))
        exp_at = now + timedelta(seconds=300)

        claims = {
            'iss': ISSUER,
            'aud': API_AUDIENCE,
            'sub': '6969',
            'iat': now.total_seconds(),
            'exp': exp_at.total_seconds()
        }
        token = generate_jwt(claims, priv_key)
        with pytest.raises(JsonApiException):
            util.verify_token(token, jwks)

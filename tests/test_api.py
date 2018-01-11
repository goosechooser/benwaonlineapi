import json
from datetime import datetime, timedelta
import pytest
from jose import jwt
import requests_mock
from flask_restless import ProcessingException
from flask import url_for, current_app

headers = {'Accept': 'application/vnd.api+json',
                'Content-Type': 'application/vnd.api+json'}

def get_pem(fname):
    with open(fname, 'r') as f:
        return f.read()

with open('keys/test_jwks.json', 'r') as f:
    JWKS = json.load(f)

PRIV_KEY = get_pem('keys/benwaonline_api_test_priv.pem')
PUB_KEY = get_pem('keys/benwaonline_api_test_pub.pem')
ISSUER = 'issuer'
API_AUDIENCE = 'api audience'

def generate_jwt(claims):
    ''' Generates a JWT'''
    headers = {
        'typ': 'JWT',
        'alg': 'RS256',
        'kid': 'benwaonline_api_test'
    }
    return jwt.encode(claims, PRIV_KEY, algorithm='RS256', headers=headers)

def test_authenticate_no_header(client):
    resp = client.get('/api/users', headers=headers)

    assert resp.status_code == 401
    assert 'authorization header is expected' in resp.json['errors'][0]['detail']

def test_authenticate_invalid_header(client):
    headers['Authorization'] = 'Wrong Type'
    resp = client.get('/api/users', headers=headers)

    assert resp.status_code == 401
    assert 'authorization header must start with Bearer' in resp.json['errors'][0]['detail']

    headers['Authorization'] = 'Bearer Wrong Type'
    resp = client.get('/api/users', headers=headers)

    assert resp.status_code == 401
    assert 'authorization header must be Bearer token' in resp.json['errors'][0]['detail']

def test_authenticate_no_token(client):
    headers['Authorization'] = 'Bearer'
    resp = client.get('/api/users', headers=headers)

    assert resp.status_code == 401
    assert 'token not found' in resp.json['errors'][0]['detail']

def test_authenticate_invalid_audience(client):
    claims = {
        'iss': ISSUER,
        'aud': 'invalid'
    }

    token = generate_jwt(claims)
    headers['Authorization'] = 'Bearer ' + token
    with requests_mock.Mocker() as mock:
        mock.get(current_app.config['JWKS_URL'], json=JWKS)
        resp = client.get('/api/users', headers=headers)

    assert resp.status_code == 401
    assert 'Invalid audience' in resp.json['errors'][0]['detail']

def test_authenticate_invalid_issuer(client):
    claims = {
        'iss': 'invalid',
        'aud': API_AUDIENCE,
    }

    token = generate_jwt(claims)
    headers['Authorization'] = 'Bearer ' + token
    with requests_mock.Mocker() as mock:
        mock.get(current_app.config['JWKS_URL'], json=JWKS)
        resp = client.get('/api/users', headers=headers)

    assert resp.status_code == 401
    assert 'Invalid issuer' in resp.json['errors'][0]['detail']

def test_authenticate_expired_token(client):
    now = (datetime(1971, 1, 1) - datetime(1970, 1, 1))
    exp_at = now + timedelta(seconds=0)

    claims = {
        'iss': ISSUER,
        'aud': API_AUDIENCE,
        'sub': '6969',
        'iat': now.total_seconds(),
        'exp': exp_at.total_seconds()
    }

    token = generate_jwt(claims)
    headers['Authorization'] = 'Bearer ' + token
    with requests_mock.Mocker() as mock:
        mock.get(current_app.config['JWKS_URL'], json=JWKS)
        resp = client.get('/api/users', headers=headers)

    assert resp.status_code == 401
    assert 'Signature has expired.' in resp.json['errors'][0]['detail']

def test_authenticate(client, session):
    now = (datetime.utcnow() - datetime(1970, 1, 1))
    exp_at = now + timedelta(seconds=69)

    claims = {
        'iss': ISSUER,
        'aud': API_AUDIENCE,
        'sub': '6969',
        'iat': now.total_seconds(),
        'exp': exp_at.total_seconds()
    }

    token = generate_jwt(claims)
    headers['Authorization'] = 'Bearer ' + token
    with requests_mock.Mocker() as mock:
        mock.get(current_app.config['JWKS_URL'], json=JWKS)
        resp = client.get('/api/users', headers=headers)

    assert resp.status_code == 200
    assert resp.json['meta']['total'] == 0

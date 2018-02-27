import json
from datetime import datetime, timedelta
import pytest
from jose import jwt
import requests
import requests_mock
from flask import url_for, current_app
from benwaonlineapi import schemas, models
from marshmallow import pprint

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

# IT TURNS OUT THE DATA FORMAT IS CHECKED FIRST
# SO YOU CANT SEND A POST WITH NOTHING
# BECAUSE YOU'LL GET AN ERROR
def test_authenticate_no_header(client):
    post = schemas.PostSchema().dumps({
        "id": "420"
    }).data
    resp = client.post(url_for('api.posts_list'),
                       headers=headers, data=post)
    assert resp.status_code == 401
    assert 'authorization header is expected' in resp.json['errors'][0]['detail']

def test_authenticate_invalid_header(client):
    headers['Authorization'] = 'Wrong Type'
    post = schemas.PostSchema().dumps({
        "id": "420"
    }).data
    resp = client.post(url_for('api.posts_list'),
                       headers=headers, data=post)

    assert resp.status_code == 401
    assert 'authorization header must start with Bearer' in resp.json['errors'][0]['detail']

    headers['Authorization'] = 'Bearer Wrong Type'
    resp = client.post(url_for('api.posts_list'),
                       headers=headers, data=post)

    assert resp.status_code == 401
    assert 'authorization header must be Bearer token' in resp.json['errors'][0]['detail']

def test_authenticate_no_token(client):
    headers['Authorization'] = 'Bearer'
    post = schemas.PostSchema().dumps({
        "id": "420"
    }).data
    resp = client.post(url_for('api.posts_list'),
                       headers=headers, data=post)

    assert resp.status_code == 401
    assert 'token not found' in resp.json['errors'][0]['detail']

def test_authenticate_invalid_audience(client):
    claims = {
        'iss': ISSUER,
        'aud': 'invalid'
    }

    token = generate_jwt(claims)
    headers['Authorization'] = 'Bearer ' + token
    post = schemas.PostSchema().dumps({
        "id": "420"
    }).data

    with requests_mock.Mocker() as mock:
        mock.get(current_app.config['JWKS_URL'], json=JWKS)
        resp = client.post(url_for('api.posts_list'),
                           headers=headers, data=post)

    assert resp.status_code == 401
    assert 'Invalid audience' in resp.json['errors'][0]['detail']

def test_authenticate_invalid_issuer(client):
    claims = {
        'iss': 'invalid',
        'aud': API_AUDIENCE,
    }

    token = generate_jwt(claims)
    headers['Authorization'] = 'Bearer ' + token
    post = schemas.PostSchema().dumps({
        "id": "420"
    }).data
    with requests_mock.Mocker() as mock:
        mock.get(current_app.config['JWKS_URL'], json=JWKS)
        resp = client.post(url_for('api.posts_list'),
                           headers=headers, data=post)

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
    post = schemas.PostSchema().dumps({
        "id": "420"
    }).data
    with requests_mock.Mocker() as mock:
        mock.get(current_app.config['JWKS_URL'], json=JWKS)
        resp = client.post(url_for('api.posts_list'),
                           headers=headers, data=post)

    assert resp.status_code == 401
    assert 'Signature has expired.' in resp.json['errors'][0]['detail']


def test_authenticate(client, session):
    now = (datetime.utcnow() - datetime(1970, 1, 1))
    exp_at = now + timedelta(seconds=69)

    claims = {
        'iss': ISSUER,
        'aud': API_AUDIENCE,
        'sub': '696969',
        'iat': now.total_seconds(),
        'exp': exp_at.total_seconds()
    }

    token = generate_jwt(claims)
    headers['Authorization'] = 'Bearer ' + token
    user = schemas.UserSchema().dumps({
        "id": "420",
        "username": "Beautiful Benwa Aficionado",
        # "relationships": {
        #     "likes": {
        #         "data": []
        #     }
        # }
    }).data

    with requests_mock.Mocker() as mock:
        mock.get(current_app.config['JWKS_URL'], json=JWKS)
        resp = client.post(url_for('api.users_list'), headers=headers, data=user)

    assert resp.status_code == 201
    user = schemas.UserSchema().load(resp.json).data
    assert user['id'] != 420
    assert user['user_id'] == '696969'
    resp = client.get(url_for('api.users_likes', id=1),
                       headers=headers)

    assert resp.status_code == 200

def test_create_post_with_tags(client, session):
    now = (datetime.utcnow() - datetime(1970, 1, 1))
    exp_at = now + timedelta(seconds=69)

    claims = {
        'iss': ISSUER,
        'aud': API_AUDIENCE,
        'sub': '696969',
        'iat': now.total_seconds(),
        'exp': exp_at.total_seconds()
    }

    token = generate_jwt(claims)
    headers['Authorization'] = 'Bearer ' + token
    post = schemas.PostSchema().dumps({
        "id": "420",
        "title": "why are you doing this",
        "tags": [
                {
                    'type': 'tags',
                    'id': '1'
                }
        ]
    }).data

    with requests_mock.Mocker() as mock:
        mock.get(current_app.config['JWKS_URL'], json=JWKS)
        resp = client.post(url_for('api.posts_list') + '?include=tags',
                           headers=headers, data=post)
        assert resp.status_code == 201

        resp = client.get('/api/posts/1', headers=headers)
        assert resp.status_code == 200
        resp = client.get('/api/posts/1/tags', headers=headers)
        assert resp.status_code == 200
        resp = client.get('/api/posts/1/relationships/tags', headers=headers)
        assert resp.status_code == 200

def test_delete_post(client, session):
    now = (datetime.utcnow() - datetime(1970, 1, 1))
    exp_at = now + timedelta(seconds=69)

    claims = {
        'iss': ISSUER,
        'aud': API_AUDIENCE,
        'sub': '696969',
        'iat': now.total_seconds(),
        'exp': exp_at.total_seconds()
    }

    token = generate_jwt(claims)
    headers['Authorization'] = 'Bearer ' + token

    with requests_mock.Mocker() as mock:
        mock.get(current_app.config['JWKS_URL'], json=JWKS)
        resp = client.delete(url_for('api.posts_detail', id=2), headers=headers)
        assert resp.status_code == 200

        resp = client.get('/api/posts/2', headers=headers)
        assert resp.status_code == 404
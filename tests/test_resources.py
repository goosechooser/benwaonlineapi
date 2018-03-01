import re
from datetime import datetime, timedelta
import requests
import requests_mock
import pytest
from flask import url_for, current_app, json
from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship

from benwaonlineapi import schemas
from benwaonlineapi import models
# from benwaonlineapi.resources import UserList, PostList, TagList
from benwaonlineapi.manager import manager
from tests.helpers import generate_jwt

# notes:
# Can parametrize the entire class - but tests MUST use the param
# Fixtures go inside the test class - UNLESS YOU USE THEM IN LAZY FIXTURE I GUESS

def format_url(url):
        url = re.sub('<[^>]+>', '{id}', url)
        return '/api' + url

def label(param):
    return param.resource.__name__

def relationship_label(param):
    return param.view

def categorize_urls(urls, schema):
    type_ = schema.Meta.type_
    str_len = len(type_)
    base_url = []
    related_urls = []

    for url in urls:
        if type_ in url[5:str_len+5]:
            base_url.append(url)
        else:
            related_urls.append(url)

    return base_url[0], related_urls

with open('keys/test_jwks.json', 'r') as f:
    JWKS = json.load(f)

@pytest.fixture(scope='session')
def headers():
    now = (datetime.utcnow() - datetime(1970, 1, 1))
    exp_at = now + timedelta(seconds=690000)

    claims = {
        'iss': 'issuer',
        'aud': 'api audience',
        'sub': '36420',
        'iat': now.total_seconds(),
        'exp': exp_at.total_seconds()
    }

    token = generate_jwt(claims)
    _headers = {
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json',
        'Authorization': 'Bearer ' + token
    }
    return _headers

@pytest.fixture(scope='session')
def req_mock():
    with requests_mock.Mocker(real_http=True) as mock:
        mock.get(current_app.config['JWKS_URL'], json=JWKS)
        yield mock

@pytest.fixture(scope='session')
def user(app, headers, req_mock):
    user = schemas.UserSchema().dumps({
        "id": "420",
        "username": "Beautiful Benwa Aficionado",
    }).data

    with app.test_client() as client:
        resp = client.post(url_for('api.users_list'), headers=headers, data=user)
    data = resp.json['data']

    yield data

@pytest.fixture(scope='session')
def tags(app, headers, req_mock):
    tag = schemas.TagSchema().dumps({
        'id': '1',
        'name': 'benwa'
    }).data
    with app.test_client() as client:
        resp = client.post(url_for('api.tags_list'), headers=headers, data=tag)
    data = resp.json['data']

    yield data

@pytest.fixture(scope='session')
def images(app, headers, req_mock):
    image = schemas.ImageSchema().dumps({
        "id": "420",
        "filepath": "test_image_filepath",
    }).data

    with app.test_client() as client:
        resp = client.post(url_for('api.images_list'), headers=headers, data=image)
    data = resp.json['data']

    yield data

@pytest.fixture(scope='session')
def previews(app, headers, req_mock):
    preview = schemas.PreviewSchema().dumps({
        "id": "420",
        "filepath": "test_preview_filepath",
    }).data

    with app.test_client() as client:
        resp = client.post(url_for('api.previews_list'), headers=headers, data=preview)
    data = resp.json['data']

    yield data

@pytest.fixture(scope='session')
def posts(app, headers, req_mock, tags, previews, images, user):
    post = schemas.PostSchema().dumps({
        "id": "420",
        "title": "an amazing test post",
        "tags": [
                {
                    'type': 'tags',
                    'id': tags['id']
                }
        ],
        'image': {
            'type': 'images',
            'id': images['id']
        },
        'preview': {
            'type': 'previews',
            'id': previews['id']
        },
        'user': {
            'type': 'users',
            'id': user['id']
        }
    }).data

    with app.test_client() as client:
        resp = client.post(url_for('api.posts_list') + '?include=tags,image,preview,user', headers=headers, data=post)
    print('post resp', resp.json)
    print('post data', resp.json['data'])
    data = resp.json['data']

    yield data

@pytest.fixture(scope='session')
def comments(app, headers, req_mock, user, posts):
    comment = schemas.CommentSchema().dumps({
        "id": "420",
        "content": "a wonderful test comment",
        "user": {
            'type': 'users',
            'id': user['id']
        },
        'post': {
            'type': 'posts',
            'id': posts['id']
        }
    }).data

    with app.test_client() as client:
        resp = client.post(url_for('api.comments_list') + '?include=user,post', headers=headers, data=comment)
    data = resp.json['data']

    yield data

@pytest.fixture(scope='session')
def like_post(app, headers, req_mock, user, posts):
    like = schemas.PostSchema(many=True).dumps([{
        "type": "posts",
        "id": posts['id']
    }]).data

    with app.test_client() as client:
        resp = client.post(url_for('api.users_likes', id=user['id']), headers=headers, data=like)
    data = resp.json['data']

    yield data

class RUT(object):
    def __init__(self, resource, urls, view, url_rule_options):
        self.resource = resource
        self.schema = resource.schema
        self.urls = [format_url(url) for url in urls]
        self.base_url, self.related_urls = categorize_urls(self.urls, self.schema)
        self.view = view
        self.url_rule_options = url_rule_options

resource_relationships = [RUT(**resource) for resource in filter(lambda x: issubclass(x['resource'], ResourceRelationship), manager.resources)]

@pytest.mark.usefixtures('user', 'tags', 'images', 'previews', 'posts', 'comments', 'like_post')
class TestResourceRelationshipSuite(object):
    @pytest.fixture(params=resource_relationships, ids=relationship_label)
    def resource(self, request):
        return request.param

    def test_base_url(self, client, resource):
        response = client.get(resource.base_url.format(id=1))
        assert response.status_code == 200

    @pytest.mark.parametrize("id_, has_errors", [
        (1, False),
        (420, True)
    ])
    def test_schema_format(self, client, resource, id_, has_errors):
        response = client.get(resource.base_url.format(id=id_))
        related_field = resource.base_url.split('/')[-1]
        related_resource = resource.schema._declared_fields[related_field]
        related_schema = related_resource.schema
        related_schema.many = related_resource.many
        errors = related_schema.load(response.json).errors
        assert any(errors) == has_errors

resource_details = [RUT(**resource) for resource in filter(lambda x: issubclass(x['resource'], ResourceDetail), manager.resources)]

@pytest.mark.usefixtures('user', 'tags', 'images', 'previews', 'posts', 'comments', 'like_post')
class TestResourceDetailSuite(object):
    @pytest.fixture(params=resource_details, ids=label)
    def resource(self, request):
        return request.param

    def test_base_url(self, client, resource):
        response = client.get(resource.base_url.format(id=1))
        assert response.status_code == 200

    @pytest.mark.parametrize("id_, status_code", [
        (1, 200),
        (420, 404)
    ])
    def test_related_urls(self, client, resource, id_, status_code):
        for url in resource.related_urls:
            response = client.get(url.format(id=id_))
            assert response.status_code == status_code

    @pytest.mark.parametrize("id_, has_errors", [
        (1, False),
        (420, True)
    ])
    def test_schema_format_related_urls(self, client, resource, id_, has_errors):
        for url in resource.related_urls:
            response = client.get(url.format(id=id_))
            errors = resource.schema().load(response.json).errors
            assert any(errors) == has_errors

resource_lists = [RUT(**resource) for resource in filter(lambda x: issubclass(x['resource'], ResourceList), manager.resources)]


@pytest.mark.usefixtures('user', 'tags', 'images', 'previews', 'posts', 'comments', 'like_post')
class TestResourceListSuite(object):
    @pytest.fixture(params=resource_lists, ids=label)
    def resource(self, request):
        return request.param

    def test_base_url(self, client, resource):
        response = client.get(resource.base_url)
        print('url', resource.base_url)
        assert response.status_code == 200
        print('response', response.json)

    @pytest.mark.parametrize("id_, status_code", [
        (1, 200),
        (420, 404)
    ])
    def test_related_urls(self, client, resource, id_, status_code):
        for url in resource.related_urls:
            print('url tested', url)
            response = client.get(url.format(id=id_))
            assert response.status_code == status_code

    @pytest.mark.parametrize("id_, has_errors", [
        (1, False),
        (420, True)
    ])
    def test_schema_format_related_urls(self, client, resource, id_, has_errors):
        for url in resource.related_urls:
            print('url', url)
            response = client.get(url.format(id=id_))
            print('response', response.json)
            errors = resource.schema(many=True).load(response.json).errors
            assert any(errors) == has_errors

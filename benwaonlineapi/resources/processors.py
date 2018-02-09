from functools import wraps
# import json
from jose import jwt

from flask import request
# from pymemcache.client.murmur3 import murmur3_32
from flask_rest_jsonapi.exceptions import JsonApiException
from benwaonlineapi import models
from benwaonlineapi.cache import cache
from benwaonlineapi.util import verify_token, get_jwks, has_scope

# def get_cache_key():
#     return str(murmur3_32(request.path + request.query_string.decode("utf-8")))

# def cache_preprocessor(**kwargs):
#     key = get_cache_key()
#     if cache.get(key):
#         raise JsonApiException(description=cache.get(key), code=200)

# def cache_postprocessor(result, **kwargs):
#     cache.set(get_cache_key(), json.dumps(result), expire=60)


def get_token_header():
    auth = request.headers.get('authorization', None)
    if not auth:
        raise JsonApiException(title='authorization header missing',
                                    detail='authorization header is expected',
                                    status=401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise JsonApiException(title='invalid header',
                                    detail='authorization header must start with Bearer',
                                    status=401)
    elif len(parts) == 1:
        raise JsonApiException(title='invalid header',
                                    detail='token not found',
                                    status=401)
    elif len(parts) > 2:
        raise JsonApiException(title='invalid header',
                                    detail='authorization header must be Bearer token',
                                    status=401)
    token = parts[1]
    return token

def _authenticate(*args, **kwargs):
    try:
        token = get_token_header()
        jwks = get_jwks()
        verify_token(token, jwks)
    except JsonApiException as err:
        raise err


def authenticate(api_method):
    @wraps(api_method)
    def decorator(*args, **kwargs):
        _authenticate(*args, **kwargs)
        return api_method(*args, **kwargs)
    return decorator

def remove_id(data, **kw):
    # Because marshmallow-jsonapi schemas REQUIRE id
    # but we don't allow user specified ids
    try:
        del data['id']
    except KeyError:
        pass

def username_preproc(data=None, **kw):
    ''' Preprocessor for username, used during a POST_RESOURCE of a User '''
    token = get_token_header()
    claims = jwt.get_unverified_claims(token)
    data['user_id'] = claims['sub']

def count(result=None, filters=None, sort=None, group_by=None, single=None, **kw):
    '''
    Post-processor for GET_COLLECTION of tags.
    Adds the number of posts containing the tag to the meta field.
    '''
    if not single:
        for tag in result['data']:
            _id = int(tag['id'])
            tag['meta'] = {'total': len(models.Tag.query.get(_id).posts)}

def has_permission(resource_id, **kw):
    '''
    Pre-processor for DELETE_RESOURCE
    Checks if:
        the resource being deleted is 'owned' by the requester
        the requester has admin privs/scope
    '''

    token = get_token_header()
    unverified_claims = jwt.get_unverified_claims(token)

    token_scopes = unverified_claims['scope'].split()
    if 'delete:other-comments' in token_scopes:
        return

    # Check if owner of resource
    user_id = unverified_claims['sub'].split('|')
    user = models.User.query.filter_by(user_id=user_id).first()
    is_owner = models.Comment.query.get(resource_id).owner_is(user)

    if not is_owner:
        raise JsonApiException(title='invalid header',
                                    detail='not the owner of this resource',
                                    status=401)

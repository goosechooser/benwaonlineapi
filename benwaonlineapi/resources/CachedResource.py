from flask import current_app, json, request, url_for
from redis import exceptions
from benwaonlineapi.cache import cache, murmur3_32

from flask_rest_jsonapi import (ResourceDetail, ResourceList,
                                ResourceRelationship)
from flask_rest_jsonapi.decorators import check_method_requirements


def get_cache_key():
    '''Creates a cache key from the request base path and the query string.'''
    return str(murmur3_32(request.path + request.query_string.decode("utf-8")))

class CachedList(ResourceList):
    @check_method_requirements
    def get(self, *args, **kwargs):
        """Retrieve a cached collection of objects"""
        key = get_cache_key()
        try:
            cached = cache.get(key)
        except exceptions.ConnectionError:
            msg = 'Could not connect to redis instance. Querying database.'
            current_app.logger.info(msg)
            return super(CachedList, self).get(*args, **kwargs)

        if cached:
            return cached

        result = super(CachedList, self).get(*args, **kwargs)
        cache.set(key, result, expire=60)

        return result

class CachedDetail(ResourceDetail):
    @check_method_requirements
    def get(self, *args, **kwargs):
        """Retrieve a cached collection of objects"""
        key = get_cache_key()
        try:
            cached = cache.get(key)
        except exceptions.ConnectionError:
            msg = 'Could not connect to redis instance. Querying database.'
            current_app.logger.info(msg)
            return super(CachedDetail, self).get(*args, **kwargs)

        if cached:
            return cached

        result = super(CachedDetail, self).get(*args, **kwargs)
        cache.set(get_cache_key(), result, expire=60)

        return result
import operator
import re
import pytest

from flask import url_for, current_app
from benwaonlineapi import schemas
from benwaonlineapi import models
from benwaonlineapi.manager import manager

from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship

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

class RUT(object):
    def __init__(self, resource, urls, view, url_rule_options):
        self.resource = resource
        self.schema = resource.schema
        self.urls = [format_url(url) for url in urls]
        self.base_url, self.related_urls = categorize_urls(self.urls, self.schema)
        self.view = view
        self.url_rule_options = url_rule_options

resource_relationships = [RUT(**resource) for resource in filter(lambda x: issubclass(x['resource'], ResourceRelationship), manager.resources)]
class TestResourceRelationshipSuite(object):
    @pytest.fixture(params=resource_relationships, ids=relationship_label)
    def resource(self, request):
        return request.param

    def test_base_url(self, client, resource, session):
        response = client.get(resource.base_url.format(id=1))
        assert response.status_code == 200

    @pytest.mark.parametrize("id_, has_errors", [
        (1, False),
        (420, True)
    ])
    def test_schema_format(self, client, resource, id_, has_errors, session):
        response = client.get(resource.base_url.format(id=id_))
        related_field = resource.base_url.split('/')[-1]
        related_resource = resource.schema._declared_fields[related_field]
        related_schema = related_resource.schema
        related_schema.many = related_resource.many
        errors = related_schema.load(response.json).errors
        assert any(errors) == has_errors

resource_details = [RUT(**resource) for resource in filter(lambda x: issubclass(x['resource'], ResourceDetail), manager.resources)]
class TestResourceDetailSuite(object):
    @pytest.fixture(params=resource_details, ids=label)
    def resource(self, request):
        return request.param

    def test_base_url(self, client, resource, session):
        response = client.get(resource.base_url.format(id=1))
        assert response.status_code == 200

    @pytest.mark.parametrize("id_, status_code", [
        (1, 200),
        (420, 404)
    ])
    def test_related_urls(self, client, resource, id_, status_code, session):
        for url in resource.related_urls:
            response = client.get(url.format(id=id_))
            assert response.status_code == status_code

    @pytest.mark.parametrize("id_, has_errors", [
        (1, False),
        (420, True)
    ])
    def test_schema_format_related_urls(self, client, resource, id_, has_errors, session):
        for url in resource.related_urls:
            response = client.get(url.format(id=id_))
            errors = resource.schema().load(response.json).errors
            assert any(errors) == has_errors

resource_lists = [RUT(**resource) for resource in filter(lambda x: issubclass(x['resource'], ResourceList), manager.resources)]
class TestResourceListSuite(object):
    @pytest.fixture(params=resource_lists, ids=label)
    def resource(self, request):
        return request.param

    def test_base_url(self, client, resource):
        response = client.get(resource.base_url)
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
            errors = resource.schema(many=True).load(response.json).errors
            assert any(errors) == has_errors

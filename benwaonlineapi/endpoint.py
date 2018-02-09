from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from marshmallow_jsonapi.flask import Relationship
from benwaonlineapi import schemas
from benwaonlineapi.resources import (
    PostDetail, PostList, PostRelationship,
    TagDetail, TagList, TagRelationship,
    UserDetail, UserList, UserRelationship
)

class EndpointFactory(object):
    def __init__(self):
        self.memo = {}

    @property
    def endpoints(self):
        return self.memo.values()

    def make_endpoint(self, resource):
        if issubclass(resource, ResourceDetail):
            return [self.detail_endpoint(resource)]

        if issubclass(resource, ResourceList):
            return [self.list_endpoint(resource)]

        if issubclass(resource, ResourceRelationship):
            return self.relationship_endpoint(resource)

    def relationship_endpoint(self, resource):
        # view names
        for k, v in resource.schema._declared_fields.items():
            if isinstance(v, Relationship):
                self.related_dict(resource, v, k)

    def related_dict(self, resource, related_field, related_field_name):
        # Set up the main resource
        type_ = resource.schema.Meta.type_
        view = type_ + '_' + related_field_name
        suffix = 'list' if related_field.many else 'detail'
        self.memo[view] = {'resource': resource,
                           'view': view,
                           'urls': ['/'.join(['', type_, '<int:id>', 'relationships', related_field_name])],
                           'url_rule_options': {}
                           }

        # Add related resource views to other resources
        related_view = related_field.type_ + '_' + suffix
        type_selector = '<string:type_>'
        related_url = '/'.join(['', type_selector,
                                '<int:id>', related_field_name])
        self.memo.get(related_view)['urls'].append(related_url)

    def list_endpoint(self, resource):
        type_ = resource.schema.Meta.type_
        view = type_ + '_' + 'list'
        self.memo[view] = {'resource': resource,
                           'view': view,
                           'urls': ['/'.join(['', type_])],
                           'url_rule_options': {}
                           }

    def detail_endpoint(self, resource):
        type_ = resource.schema.Meta.type_
        view = type_ + '_' + 'detail'
        self.memo[view] = {'resource': resource,
                           'view': view,
                           'urls': ['/'.join(['', type_, '<int:id>'])],
                           'url_rule_options': {}
                           }

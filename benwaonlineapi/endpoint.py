from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from marshmallow_jsonapi.flask import Relationship
from benwaonlineapi import schemas

class EndpointFactory(object):
    def __init__(self, skip=None, additional=None):
        self.memo = {}
        self.skip = skip or {}
        self.additional = additional or {}

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
        id_ = '<int:id>'
        view = type_ + '_' + related_field_name
        url = '/'.join(['', type_, id_, 'relationships', related_field_name])
        self.memoize_view(resource, view, url)

        try:
            skip_fields = self.skip[resource]
        except KeyError:
            skip_fields = []

        if related_field_name in skip_fields:
            return

        # Add related resource views to other resources
        suffix = 'list' if related_field.many else 'detail'
        related_view = related_field.type_ + '_' + suffix
        type_id = '<int:' + type_ + '_id>'
        related_url = '/'.join(['', type_,
                                type_id, related_field_name])

        self.memoize_view(resource, related_view, related_url)

    def memoize_view(self, resource, view, url):
        try:
            self.memo.get(view)['urls'].append(url)
        except TypeError:
            self.memo[view] = {
                'resource': resource,
                'view': view,
                'urls': [url],
                'url_rule_options': {}
            }

    def list_endpoint(self, resource):
        type_ = resource.schema.Meta.type_
        view = type_ + '_' + 'list'
        url = '/'.join(['', type_])

        self.memoize_view(resource, view, url)

    def detail_endpoint(self, resource):
        type_ = resource.schema.Meta.type_
        view = type_ + '_' + 'detail'
        url = '/'.join(['', type_, '<int:id>'])

        self.memoize_view(resource, view, url)

from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from marshmallow_jsonapi import fields
from benwaonlineapi import resources
from benwaonlineapi.manager import manager

# comments_api = manager.create_api(models.Comment, collection_name='comments',
#                                   methods=['GET', 'POST', 'DELETE', 'PATCH'],
#                                   allow_to_many_replacement=True)

# print(resource.view)
# print(resource.schema.Meta.type_)
# print(dir(resource.schema))
# print(manager.blueprint.name)


def view_name(resource):
    if issubclass(resource, ResourceDetail):
        suffix = '_detail'

    if issubclass(resource, ResourceList):
        suffix = '_list'

    if issubclass(resource, ResourceRelationship):
        suffix = '_relationship'

    return resource.schema.Meta.type_ + suffix

def relationship_url(relation):
    return 'relationships/' + relation.type_

def make_urls(resource):
    if issubclass(resource, ResourceDetail):
        url = resource.schema.Meta.self_url

    if issubclass(resource, ResourceList):
        url = resource.schema.Meta.type_

    if issubclass(resource, ResourceRelationship):
        for k, v in resource.schema._declared_fields.items():
            if isinstance(v, fields.Relationship):
                print(relationship_url(v))

    # return '/' + url


def endpoint_route(resource):
    print(resource.__name__)
    print(view_name(resource))
    make_urls(resource)


# def init_routes(manager, resources):
#     for resource in resources:
        # manager.route(resource, )


# class EndpointFactory(object):
#     def __init__(self, blueprint=None):
#         self.blueprint = blueprint


#     def add_route(api, resource):



if __name__ == '__main__':
    # endpoint_route(resources.PostList)
    endpoint_route(resources.PostDetail)
    # endpoint_route(resources.PostRelationship)

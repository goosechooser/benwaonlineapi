from flask import Blueprint
from flask_rest_jsonapi import Api
from benwaonlineapi.endpoint import EndpointFactory
from benwaonlineapi.resources import (
    PostDetail, PostList, PostRelationship,
    TagDetail, TagList, TagRelationship,
    UserDetail, UserList, UserRelationship,
    PreviewDetail, PreviewList, PreviewRelationship,
    ImageDetail, ImageList, ImageRelationship,
    CommentDetail, CommentList, CommentRelationship,
)

def make_endpoints(resources, endpoint_factory=None, skip=None, additional=None):
        if not endpoint_factory:
            endpoint_factory = EndpointFactory(skip, additional)

        for resource in resources:
            endpoint_factory.make_endpoint(resource)

        for k,v in additional.items():
            try:
                endpoint_factory.memo[k]['urls'].append(v)
            except TypeError:
                pass

        return endpoint_factory.endpoints

manager = Api(blueprint=Blueprint('api', __name__, url_prefix='/api'))
resources = [
    PostDetail, PostList, TagDetail,
    TagList, UserDetail, UserList,
    PreviewDetail, PreviewList, ImageDetail,
    ImageList, CommentDetail, CommentList,
    PreviewRelationship, ImageRelationship, CommentRelationship,
    UserRelationship, PostRelationship, TagRelationship
]

# resource: field
skip_related = {
    UserRelationship: ['likes'],
    PostRelationship: ['likes']
}

additional = {
    'users_list': '/posts/<int:likes_id>/likes',
    'posts_list': '/users/<int:likes_id>/likes'
}

endpoints = make_endpoints(resources, skip=skip_related, additional=additional)
manager.resources = endpoints

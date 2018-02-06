from flask import Blueprint
from flask_rest_jsonapi import Api
from benwaonlineapi.resources import (
    PostDetail, PostList, PostRelationship,
    TagDetail, TagList, TagRelationship
)

manager = Api(blueprint=Blueprint('api', __name__, url_prefix='/api'))

manager.route(PostList, 'post_list', '/posts', '/tags/<int:tag_id>/posts')
manager.route(PostDetail, 'post_detail', '/posts/<int:id>')
manager.route(PostRelationship, 'post_tags', '/posts/<int:id>/relationships/tags')
manager.route(TagList, 'tag_list', '/tags', '/posts/<int:id>/tags')
manager.route(TagDetail, 'tag_detail', '/tags/<int:id>')
manager.route(TagRelationship, 'tag_posts', '/tags/<int:id>/relationships/posts')


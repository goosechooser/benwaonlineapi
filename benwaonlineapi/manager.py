from flask import Blueprint
from flask_rest_jsonapi import Api
from benwaonlineapi.resources import (
    PostDetail, PostList, PostRelationship,
    TagDetail, TagList, TagRelationship
)

manager = Api(blueprint=Blueprint('api', __name__, url_prefix='/api'))
# THIS IS HOW U WANNA DO IT MY DUDE
test = {
    'resource': PostList,
    'view': 'post_list',
    'urls': ['/posts', '/tags/<int:id>/posts'],
    'url_rule_options': {}
}
manager.resources = [test]
# manager.route(PostList, 'post_list', '/posts', '/tags/<int:id>/posts')
manager.route(PostDetail, 'post_detail', '/posts/<int:id>')
manager.route(PostRelationship, 'post_tags', '/posts/<int:id>/relationships/tags')
manager.route(TagList, 'tag_list', '/tags', '/posts/<int:id>/tags')
manager.route(TagDetail, 'tag_detail', '/tags/<int:id>')
manager.route(TagRelationship, 'tag_posts', '/tags/<int:id>/relationships/posts')


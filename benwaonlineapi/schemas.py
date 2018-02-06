from marshmallow import post_load, pre_dump
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship
# class BaseSchema(Schema):

#     @pre_dump
#     def clean(self, data):
#         # Filter out keys with null values
#         return dict((k, v) for k, v in data.items() if v)

# class PreviewSchema(Schema):
#     id = fields.Int()
#     filepath = fields.Str()
#     created_on = fields.DateTime()

#     class Meta:
#         type_ = 'previews'
#         self_url = '/api/previews/{preview_id}'
#         self_url_kwargs = {'preview_id': '<id>'}
#         self_url_many = '/api/previews'

# class ImageSchema(Schema):
#     id = fields.Int()
#     filepath = fields.Str()
#     created_on = fields.DateTime()

#     class Meta:
#         type_ = 'images'
#         self_url = '/api/images/{image_id}'
#         self_url_kwargs = {'image_id': '<id>'}
#         self_url_many = '/api/images'

# class CommentSchema(Schema):
#     id = fields.Int()
#     content = fields.String()
#     created_on = fields.DateTime()
#     poster = fields.String(load_only=True)

#     class Meta:
#         type_ = 'comments'
#         self_url = '/api/comments/{comment_id}'
#         self_url_kwargs = {'comment_id': '<id>'}
#         self_url_many = '/api/comments'

#     user = fields.Relationship(
#         type_='users',
#         self_url = '/api/comments/{comment_id}/relationships/user',
#         self_url_kwargs = {'comment_id': '<id>'},
#         related_url='/api/comments/{comment_id}/user',
#         related_url_kwargs={'comment_id': '<id>'},
#         include_resource_linkage=True,
#         schema='UserSchema'
#     )

#     post = fields.Relationship(
#         type_='posts',
#         self_url = '/api/comments/{comment_id}/relationships/post',
#         self_url_kwargs = {'comment_id': '<id>'},
#         related_url='/api/comments/{comment_id}/post',
#         related_url_kwargs={'comment_id': '<id>'},
#         include_resource_linkage=True,
#         schema='PostSchema'
#     )

# class UserSchema(Schema):
#     id = fields.Int()
#     username = fields.String()
#     created_on = fields.DateTime()
#     user_id = fields.String(dump_only=True)
#     active = fields.Boolean(load_from='is_active', dump_to='is_active')

#     class Meta:
#         type_ = 'users'
#         self_url = '/api/users/{user_id}'
#         self_url_kwargs = {'user_id': '<id>'}

#     comments = fields.Relationship(
#         type_='comments',
#         self_url = '/api/users/{user_id}/relationships/comments',
#         self_url_kwargs = {'user_id': '<id>'},
#         related_url = '/api/users/{user_id}/comments',
#         related_url_kwargs = {'user_id': '<id>'},
#         many=True,
#         include_resource_linkage=True,
#         schema='CommentSchema'
#     )

#     posts = fields.Relationship(
#         type_='posts',
#         self_url = '/api/users/{user_id}/relationships/posts',
#         self_url_kwargs = {'user_id': '<id>'},
#         related_url = '/api/users/{user_id}/posts',
#         related_url_kwargs = {'user_id': '<id>'},
#         many=True,
#         include_resource_linkage=True,
#         schema='PostSchema'
#     )

#     likes = fields.Relationship(
#         type_='posts',
#         self_url='/api/users/{user_id}/relationships/likes',
#         self_url_kwargs={'user_id': '<id>'},
#         related_url='/api/users/{user_id}/likes',
#         related_url_kwargs={'user_id': '<id>'},
#         many=True,
#         include_resource_linkage=True,
#         schema='PostSchema'
#     )

class PostSchema(Schema):
    id = fields.Int()
    title = fields.String()
    created_on = fields.DateTime()

    class Meta:
        type_ = 'posts'
        self_view = 'api.post_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.post_list'

    # user = fields.Relationship(
    #     type_='users',
    #     self_url = '/api/posts/{post_id}/relationships/user',
    #     self_url_kwargs = {'post_id': '<id>'},
    #     related_url='/api/posts/{post_id}/user',
    #     related_url_kwargs={'post_id': '<id>'},
    #     include_resource_linkage=True,
    #     schema='UserSchema'
    # )

    # comments = fields.Relationship(
    #     type_='comments',
    #     self_url='/api/posts/{post_id}/relationships/comments',
    #     self_url_kwargs={'post_id': '<id>'},
    #     related_url='/api/posts/{post_id}/comments',
    #     related_url_kwargs={'post_id': '<id>'},
    #     many=True,
    #     include_resource_linkage=True,
    #     schema='CommentSchema'
    # )

    # image = fields.Relationship(
    #     type_='images',
    #     self_url = '/api/posts/{post_id}/relationships/image',
    #     self_url_kwargs = {'post_id': '<id>'},
    #     related_url='/api/posts/{post_id}/image',
    #     related_url_kwargs={'post_id': '<id>'},
    #     include_resource_linkage=True,
    #     schema='ImageSchema'
    # )

    # preview = fields.Relationship(
    #     type_='previews',
    #     self_url = '/api/posts/{post_id}/relationships/preview',
    #     self_url_kwargs = {'post_id': '<id>'},
    #     related_url='/api/posts/{post_id}/preview',
    #     related_url_kwargs={'post_id': '<id>'},
    #     include_resource_linkage=True,
    #     schema='PreviewSchema'
    # )

    tags = Relationship(
        type_='tags',
        self_view='api.post_tags',
        self_view_kwargs={'id': '<id>'},
        related_view='api.tag_list',
        related_view_kwargs={'id': '<id>'},
        many=True,
        include_resource_linkage=True,
        schema='TagSchema'
    )

    # likes = fields.Relationship(
    #     type_='users',
    #     self_url='/api/posts/{post_id}/relationships/likes',
    #     self_url_kwargs={'post_id': '<id>'},
    #     related_url='/api/posts/{post_id}/likes',
    #     related_url_kwargs={'post_id': '<id>'},
    #     many=True,
    #     include_resource_linkage=True,
    #     schema='UserSchema'
    # )

class TagSchema(Schema):
    id = fields.String()
    name = fields.String()
    created_on = fields.DateTime()
    # metadata = fields.Meta()

    posts = Relationship(
        type_='posts',
        self_view='api.tag_posts',
        self_view_kwargs={'id': '<id>'},
        related_view='api.post_list',
        related_view_kwargs={'id': '<id>'},
        many=True,
        include_resource_linkage=True,
        schema='PostSchema'
    )

    class Meta:
        type_ = 'tags'
        self_view = 'api.tag_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.tag_list'

    # @post_load
    # def append_total(self, data):
    #     data['total'] = data.get('metadata', {}).get('total', 1)

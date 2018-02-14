from marshmallow import post_load, pre_dump
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship

class PreviewSchema(Schema):
    id = fields.Int()
    filepath = fields.Str()
    created_on = fields.DateTime()

    class Meta:
        type_ = 'previews'
        self_view = 'api.previews_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.previews_list'

class ImageSchema(Schema):
    id = fields.Int()
    filepath = fields.Str()
    created_on = fields.DateTime()

    class Meta:
        type_ = 'images'
        self_view = 'api.images_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.images_list'

class CommentSchema(Schema):
    id = fields.Int()
    content = fields.String()
    created_on = fields.DateTime()
    poster = fields.String()

    class Meta:
        type_ = 'comments'
        self_view = 'api.comments_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.comments_list'

    user = Relationship(
        type_='users',
        self_view='api.comments_user',
        self_view_kwargs={'id': '<id>'},
        related_view='api.users_detail',
        related_view_kwargs={Meta.type_ + '_id': '<id>'},
        include_resource_linkage=True,
        schema='UserSchema'
    )

    post = Relationship(
        type_='posts',
        self_view='api.comments_post',
        self_view_kwargs={'id': '<id>'},
        related_view='api.posts_detail',
        related_view_kwargs={Meta.type_ + '_id': '<id>'},
        include_resource_linkage=True,
        schema='PostSchema'
    )

class UserSchema(Schema):
    id = fields.Int()
    username = fields.String()
    created_on = fields.DateTime()
    user_id = fields.String()
    active = fields.Boolean(load_from='is_active', dump_to='is_active')

    class Meta:
        type_ = 'users'
        self_view = 'api.users_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.users_list'

    posts = Relationship(
        type_='posts',
        self_view='api.users_posts',
        self_view_kwargs={'id': '<id>'},
        related_view='api.posts_list',
        related_view_kwargs={Meta.type_ + '_id': '<id>'},
        many=True,
        include_resource_linkage=True,
        schema='PostSchema'
    )

    comments = Relationship(
        type_='comments',
        self_view='api.users_comments',
        self_view_kwargs={'id': '<id>'},
        related_view='api.comments_list',
        related_view_kwargs={Meta.type_ + '_id': '<id>'},
        many=True,
        include_resource_linkage=True,
        schema='CommentSchema'
    )

    likes = Relationship(
        type_='likes',
        self_view='api.users_likes',
        self_view_kwargs={'id': '<id>'},
        related_kwargs='api.posts_list',
        related_view_kwargs={Meta.type_ + '_id': '<id>'},
        many=True,
        include_resource_linkage=True,
        schema='PostSchema'
    )

class PostSchema(Schema):
    id = fields.Int()
    title = fields.String()
    created_on = fields.DateTime()

    class Meta:
        type_ = 'posts'
        self_view = 'api.posts_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.posts_list'

    tags = Relationship(
        type_='tags',
        self_view='api.posts_tags',
        self_view_kwargs={'id': '<id>'},
        related_view='api.tags_list',
        related_view_kwargs={Meta.type_ + '_id': '<id>'},
        many=True,
        include_resource_linkage=True,
        schema='TagSchema'
    )

    user = Relationship(
        type_='users',
        self_view='api.posts_user',
        self_view_kwargs={'id': '<id>'},
        related_view='api.users_detail',
        related_view_kwargs={Meta.type_ + '_id': '<id>'},
        include_resource_linkage=True,
        schema='UserSchema'
    )

    image = Relationship(
        type_='images',
        self_view='api.posts_image',
        self_view_kwargs={'id': '<id>'},
        related_view='api.images_detail',
        related_view_kwargs={'id': '<id>'},
        include_resource_linkage=True,
        schema='ImageSchema'
    )

    preview = Relationship(
        type_='previews',
        self_view='api.posts_preview',
        self_view_kwargs={'id': '<id>'},
        related_view='api.previews_detail',
        related_view_kwargs={'id': '<id>'},
        include_resource_linkage=True,
        schema='PreviewSchema'
    )

    comments = Relationship(
        type_='comments',
        self_view='api.posts_comments',
        self_view_kwargs={'id': '<id>'},
        related_view='api.comments_list',
        related_view_kwargs={Meta.type_ + '_id': '<id>'},
        many=True,
        include_resource_linkage=True,
        schema='CommentSchema'
    )

    likes = Relationship(
        type_='likes',
        self_view='api.posts_likes',
        self_view_kwargs={'id': '<id>'},
        related_view='api.likes_list',
        related_view_kwargs={Meta.type_ + '_id': '<id>'},
        many=True,
        include_resource_linkage=True,
        schema='UserSchema'
    )

class LikesSchema(Schema):
    id = fields.Int()
    class Meta:
        type_ = 'likes'
        self_view = 'api.likes_list'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.likes_list'

class TagSchema(Schema):
    id = fields.String()
    name = fields.String()
    created_on = fields.DateTime()
    num_posts = fields.Int()

    class Meta:
        type_ = 'tags'
        self_view = 'api.tags_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.tags_list'

    posts = Relationship(
        type_='posts',
        self_view='api.tags_posts',
        self_view_kwargs={'id': '<id>'},
        related_view='api.posts_list',
        related_view_kwargs={Meta.type_ + '_id': '<id>'},
        many=True,
        include_resource_linkage=True,
        schema='PostSchema'
    )

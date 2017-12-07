from marshmallow import post_load
from marshmallow_jsonapi import Schema, fields
from benwaonlineapi.models import User, Image, Preview, Comment, Post, Tag

class PreviewSchema(Schema):
    id = fields.Int(dump_only=True)
    filepath = fields.Str()
    created_on = fields.DateTime()

    class Meta:
        type_ = 'previews'
        strict = True
        self_url = '/api/previews/{preview_id}'
        self_url_kwargs = {'preview_id': '<id>'}

    @post_load
    def make_preview(self, data):
        return Preview(**data)

class ImageSchema(Schema):
    id = fields.Int(dump_only=True)
    filepath = fields.Str()
    created_on = fields.DateTime()

    class Meta:
        type_ = 'images'
        strict = True
        self_url = '/api/images/{image_id}'
        self_url_kwargs = {'image_id': '<id>'}

    @post_load
    def make_image(self, data):
        return Image(**data)

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.String()
    created_on = fields.DateTime()

    class Meta:
        type_ = 'comments'
        fields = ('id', 'content', 'created_on', 'user', 'post')
        strict = True
        self_url = '/api/comments/{comment_id}'
        self_url_kwargs = {'comment_id': '<id>'}

    user = fields.Relationship(
        type_='users',
        self_url = '/api/comments/{comment_id}/relationships/user',
        self_url_kwargs = {'comment_id': '<id>'},
        related_url='/api/comments/{comment_id}/user',
        related_url_kwargs={'comment_id': '<id>'},
        include_resource_linkage=True,
        schema='UserSchema'
    )

    post = fields.Relationship(
        type_='posts',
        self_url = '/api/comments/{comment_id}/relationships/post',
        self_url_kwargs = {'comment_id': '<id>'},
        related_url='/api/comments/{comment_id}/post',
        related_url_kwargs={'comment_id': '<id>'},
        include_resource_linkage=True,
        schema='PostSchema'
    )

    # @post_load
    # def make_comment(self, data):
    #     return Comment(**data)

class UserSchema(Schema):
    id = fields.Int()
    username = fields.String()
    created_on = fields.DateTime()
    user_id = fields.String(dump_only=True)
    active = fields.Boolean()

    class Meta:
        type_ = 'users'
        strict = True
        self_url = '/api/users/{user_id}'
        self_url_kwargs = {'user_id': '<id>'}

    comments = fields.Relationship(
        dump_only=True,
        type_='comments',
        self_url = '/api/users/{user_id}/relationships/comments',
        self_url_kwargs = {'user_id': '<id>'},
        related_url = '/api/users/{user_id}/comments',
        related_url_kwargs = {'user_id': '<id>'},
        many=True,
        include_resource_linkage=False,
        schema='CommentSchema'
    )

    posts = fields.Relationship(
        dump_only=True,
        type_='posts',
        self_url = '/api/users/{user_id}/relationships/posts',
        self_url_kwargs = {'user_id': '<id>'},
        related_url = '/api/users/{user_id}/posts',
        related_url_kwargs = {'user_id': '<id>'},
        many=True,
        include_resource_linkage=False,
        schema='PostSchema'
    )

    @post_load
    def make_user(self, data):
        return User(**data)

class PostSchema(Schema):
    id = fields.Int()
    title = fields.String()
    created_on = fields.DateTime()

    class Meta:
        type_ = 'posts'
        fields = ('id', 'title', 'created_on', 'user', 'comments', 'image', 'preview', 'tags')
        strict = True
        self_url = '/api/posts/{post_id}'
        self_url_kwargs = {'post_id': '<id>'}

    user = fields.Relationship(
        type_='users',
        self_url = '/api/posts/{post_id}/relationships/user',
        self_url_kwargs = {'post_id': '<id>'},
        related_url='/api/posts/{post_id}/user',
        related_url_kwargs={'post_id': '<id>'},
        include_resource_linkage=True,
        schema='UserSchema'
    )

    comments = fields.Relationship(
        type_='comments',
        self_url='/api/posts/{post_id}/relationships/comments',
        self_url_kwargs={'post_id': '<id>'},
        related_url='/api/posts/{post_id}/comments',
        related_url_kwargs={'post_id': '<id>'},
        many=True,
        include_resource_linkage=True,
        schema='CommentSchema'
    )

    image = fields.Relationship(
        type_='images',
        self_url = '/api/posts/{post_id}/relationships/image',
        self_url_kwargs = {'post_id': '<id>'},
        related_url='/api/posts/{post_id}/image',
        related_url_kwargs={'post_id': '<id>'},
        include_resource_linkage=True,
        schema='ImageSchema'
    )

    preview = fields.Relationship(
        type_='previews',
        self_url = '/api/posts/{post_id}/relationships/preview',
        self_url_kwargs = {'post_id': '<id>'},
        related_url='/api/posts/{post_id}/preview',
        related_url_kwargs={'post_id': '<id>'},
        include_resource_linkage=True,
        schema='PreviewSchema'
    )

    tags = fields.Relationship(
        type_='tags',
        self_url='/api/posts/{post_id}/relationships/tags',
        self_url_kwargs={'post_id': '<id>'},
        related_url='/api/posts/{post_id}/tags',
        related_url_kwargs={'post_id': '<id>'},
        many=True,
        include_resource_linkage=True,
        schema='TagSchema'
    )

    # @post_load
    # def make_post(self, data):
    #     return Post(**data)

class TagSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String()
    created_on = fields.DateTime()
    metadata = fields.Meta()

    posts = fields.Relationship(
        type_='posts',
        self_url = '/api/tags/{tag_id}/relationships/posts',
        self_url_kwargs = {'tag_id': '<id>'},
        related_url = '/api/tags/{tag_id}/posts',
        related_url_kwargs = {'tag_id': '<id>'},
        many=True,
        include_resource_linkage=True,
        schema='PostSchema'
    )

    class Meta:
        type_ = 'tags'
        fields = ('id', 'name', 'created_on', 'posts')
        # strict = True
        self_url = '/api/tags/{tag_id}'
        self_url_kwargs = {'tag_id': '<id>'}

    # @post_load
    # def make_tag(self, data):
    #     return Tag(**data)

from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from benwaonlineapi.database import db
from benwaonlineapi import schemas
from benwaonlineapi import models

class PostList(ResourceList):
    view_kwargs = True
    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post
    }

class PostDetail(ResourceDetail):
    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post
    }

class PostRelationship(ResourceRelationship):
    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post,
    }

class TagList(ResourceList):
    view_kwargs = True
    schema = schemas.TagSchema
    data_layer = {
        'session': db.session,
        'model': models.Tag
    }

class TagDetail(ResourceDetail):
    schema = schemas.TagSchema
    data_layer = {
        'session': db.session,
        'model': models.Tag
    }

class TagRelationship(ResourceRelationship):
    schema = schemas.TagSchema
    data_layer = {
        'session': db.session,
        'model': models.Tag
    }

class UserList(ResourceList):
    view_kwargs = True
    schema = schemas.UserSchema
    data_layer = {
        'session': db.session,
        'model': models.User
    }

class UserDetail(ResourceDetail):
    schema = schemas.UserSchema
    data_layer = {
        'session': db.session,
        'model': models.User
    }

class UserRelationship(ResourceRelationship):
    schema = schemas.UserSchema
    data_layer = {
        'session': db.session,
        'model': models.User
    }

class ImageList(ResourceList):
    view_kwargs = True
    schema = schemas.ImageSchema
    data_layer = {
        'session': db.session,
        'model': models.Image
    }

class ImageDetail(ResourceDetail):
    schema = schemas.ImageSchema
    data_layer = {
        'session': db.session,
        'model': models.Image
    }

class ImageRelationship(ResourceRelationship):
    schema = schemas.ImageSchema
    data_layer = {
        'session': db.session,
        'model': models.Image
    }

class PreviewList(ResourceList):
    view_kwargs = True
    schema = schemas.PreviewSchema
    data_layer = {
        'session': db.session,
        'model': models.Preview
    }

class PreviewDetail(ResourceDetail):
    schema = schemas.PreviewSchema
    data_layer = {
        'session': db.session,
        'model': models.Preview
    }

class PreviewRelationship(ResourceRelationship):
    schema = schemas.PreviewSchema
    data_layer = {
        'session': db.session,
        'model': models.Preview
    }

class CommentList(ResourceList):
    view_kwargs = True
    schema = schemas.CommentSchema
    data_layer = {
        'session': db.session,
        'model': models.Comment
    }

class CommentDetail(ResourceDetail):
    schema = schemas.CommentSchema
    data_layer = {
        'session': db.session,
        'model': models.Comment
    }

class CommentRelationship(ResourceRelationship):
    schema = schemas.CommentSchema
    data_layer = {
        'session': db.session,
        'model': models.Comment
    }

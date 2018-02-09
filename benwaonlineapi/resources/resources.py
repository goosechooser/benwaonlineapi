from jose import jwt
from flask import request, current_app
from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound
from benwaonlineapi.database import db
from benwaonlineapi import schemas
from benwaonlineapi import models
# from benwaonlineapi.util import verify_token, get_jwks
from benwaonlineapi.resources import processors

class BaseList(ResourceList):
    @processors.authenticate
    def before_post(self, *args, **kwargs):
        processors.remove_id(kwargs['data'])
        pass

class BaseDetail(ResourceDetail):
    @processors.authenticate
    def before_patch(self, *args, **kwargs):
        pass

    @processors.authenticate
    def before_delete(self, *args, **kwargs):
        pass

class BaseRelationship(ResourceRelationship):
    @processors.authenticate
    def before_post(self, *args, **kwargs):
        pass

    @processors.authenticate
    def before_patch(self, *args, **kwargs):
        pass

    @processors.authenticate
    def before_delete(self, *args, **kwargs):
        pass

class PostList(BaseList):
    view_kwargs = True
    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post
    }

class PostDetail(BaseDetail):
    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post
    }

class PostRelationship(BaseRelationship):
    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post,
    }

class PostRelationship(BaseRelationship):
    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post,
    }

class LikeDetail(PostDetail):
    # schema = schemas.LikesSchema
    pass

class LikeList(PostList):
    # schema = schemas.LikesSchema
    pass

class LikeRelationship(PostRelationship):
    # schema = schemas.LikesSchema
    pass

class TagList(BaseList):
    view_kwargs = True
    schema = schemas.TagSchema
    data_layer = {
        'session': db.session,
        'model': models.Tag
    }

class TagDetail(BaseDetail):
    schema = schemas.TagSchema
    data_layer = {
        'session': db.session,
        'model': models.Tag
    }

class TagRelationship(BaseRelationship):
    schema = schemas.TagSchema
    data_layer = {
        'session': db.session,
        'model': models.Tag
    }

class UserList(BaseList):
    @processors.authenticate
    def before_post(self, *args, **kwargs):
        processors.remove_id(kwargs['data'])
        processors.username_preproc(kwargs['data'])

    view_kwargs = True
    schema = schemas.UserSchema
    data_layer = {
        'session': db.session,
        'model': models.User
    }

class UserDetail(BaseDetail):
    def before_get_object(self, view_kwargs):
        if view_kwargs.get('id') is not None:
            try:
                user = self.session.query(self.model).filter_by(id=view_kwargs['id']).one()

            except NoResultFound:
                raise ObjectNotFound({'parameter': 'id'},
                                     "Entry: {} not found".format(view_kwargs['id']))

    schema = schemas.UserSchema
    data_layer = {
        'session': db.session,
        'model': models.User,
        'methods': {'before_get_object': before_get_object}
    }

class UserRelationship(BaseRelationship):
    schema = schemas.UserSchema
    data_layer = {
        'session': db.session,
        'model': models.User
    }

class ImageList(BaseList):
    view_kwargs = True
    schema = schemas.ImageSchema
    data_layer = {
        'session': db.session,
        'model': models.Image
    }

class ImageDetail(BaseDetail):
    schema = schemas.ImageSchema
    data_layer = {
        'session': db.session,
        'model': models.Image
    }

class ImageRelationship(BaseRelationship):
    schema = schemas.ImageSchema
    data_layer = {
        'session': db.session,
        'model': models.Image
    }

class PreviewList(BaseList):
    view_kwargs = True
    schema = schemas.PreviewSchema
    data_layer = {
        'session': db.session,
        'model': models.Preview
    }

class PreviewDetail(BaseDetail):
    schema = schemas.PreviewSchema
    data_layer = {
        'session': db.session,
        'model': models.Preview
    }

class PreviewRelationship(BaseRelationship):
    schema = schemas.PreviewSchema
    data_layer = {
        'session': db.session,
        'model': models.Preview
    }

class CommentList(BaseList):
    view_kwargs = True
    schema = schemas.CommentSchema
    data_layer = {
        'session': db.session,
        'model': models.Comment
    }

class CommentDetail(BaseDetail):
    schema = schemas.CommentSchema
    data_layer = {
        'session': db.session,
        'model': models.Comment
    }

class CommentRelationship(BaseRelationship):
    schema = schemas.CommentSchema
    data_layer = {
        'session': db.session,
        'model': models.Comment
    }

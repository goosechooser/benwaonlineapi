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

class PostList(ResourceList):
    def before_create_object(self, data, view_kwargs):
        processors.remove_id(data)

    view_kwargs = True
    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post,
        'methods': {
            'before_create_object': before_create_object
        }
    }

    @processors.authenticate
    def before_post(*args, **kwargs):
    #    """Make custom work here. View args and kwargs are provided as parameter
    #    """
       msg = 'args: {}\nkwargs: {}'.format(args, kwargs)
       current_app.logger.debug(msg)

class PostDetail(ResourceDetail):
    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post
    }

    def before_get(*args, **kwargs):
       """Make custom work here. View args and kwargs are provided as parameter
       """
       print('??')
       print(request.headers)
       msg = 'args: {}\nkwargs: {}'.format(args, kwargs)
       current_app.logger.debug(msg)
       processors.authenticate(*args, **kwargs)

    def before_post(*args, **kwargs):
       """Make custom work here. View args and kwargs are provided as parameter
       """
       print('??')
       print(request.headers)
       msg = 'args: {}\nkwargs: {}'.format(args, kwargs)
       current_app.logger.debug(msg)
       processors.authenticate(*args, **kwargs)

class PostRelationship(ResourceRelationship):
    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post,
    }

class TagList(ResourceList):
    def before_create_object(self, data, view_kwargs):
        print('LIST before_create_object', data, view_kwargs)
        processors.remove_id(data)

    view_kwargs = True
    schema = schemas.TagSchema
    data_layer = {
        'session': db.session,
        'model': models.Tag,
        'methods': {'before_create_object': before_create_object}

    }

    def before_post(*args, **kwargs):
       """Make custom work here. View args and kwargs are provided as parameter
       """
       print('??')
       print(request.headers)
       msg = 'args: {}\nkwargs: {}'.format(args, kwargs)
       current_app.logger.debug(msg)
       processors.authenticate(*args, **kwargs)

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
    def before_create_object(self, data, view_kwargs):
        print('LIST before_create_object', data, view_kwargs)
        processors.remove_id(data)
        processors.username_preproc(data)

    view_kwargs = True
    schema = schemas.UserSchema
    data_layer = {
        'session': db.session,
        'model': models.User,
        'methods': {'before_create_object': before_create_object}
    }

class UserDetail(ResourceDetail):
    def before_create_object(self, data, view_kwargs):
        print('before_create_object', data, view_kwargs)
        # del view_kwargs['id']
        # raise Exception

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
        'methods': {'before_create_object': before_create_object,
                    'before_get_object': before_get_object}
    }

class UserRelationship(ResourceRelationship):
    schema = schemas.UserSchema
    data_layer = {
        'session': db.session,
        'model': models.User
    }

class ImageList(ResourceList):
    def before_create_object(self, data, view_kwargs):
        print('LIST before_create_object', data, view_kwargs)
        processors.remove_id(data)

    view_kwargs = True
    schema = schemas.ImageSchema
    data_layer = {
        'session': db.session,
        'model': models.Image,
        'methods': {'before_create_object': before_create_object}

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
    def before_create_object(self, data, view_kwargs):
        print('LIST before_create_object', data, view_kwargs)
        processors.remove_id(data)

    view_kwargs = True
    schema = schemas.PreviewSchema
    data_layer = {
        'session': db.session,
        'model': models.Preview,
        'methods': {'before_create_object': before_create_object}

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
    def before_create_object(self, data, view_kwargs):
        print('LIST before_create_object', data, view_kwargs)
        processors.remove_id(data)

    view_kwargs = True
    schema = schemas.CommentSchema
    data_layer = {
        'session': db.session,
        'model': models.Comment,
        'methods': {'before_create_object': before_create_object}

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

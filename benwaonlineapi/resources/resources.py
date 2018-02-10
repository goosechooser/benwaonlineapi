from jose import jwt
from flask import request, current_app
from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.inspection import inspect

from benwaonlineapi.database import db
from benwaonlineapi import schemas
from benwaonlineapi import models
from benwaonlineapi.resources import processors

#source - https://stackoverflow.com/questions/11668355/sqlalchemy-get-model-from-table-name-this-may-imply-appending-some-function-to
def get_class_by_tablename(tablename):
    """Return class reference mapped to table.

    :param tablename: String with name of table.
    :return: Class reference or None.
    """
    for c in db.Model._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c
    return None

class BaseList(ResourceList):
    view_kwargs = True
    attrs = {}

    @processors.authenticate
    def before_post(self, *args, **kwargs):
        processors.remove_id(kwargs['data'])
        pass

    def query(self, view_kwargs):
        ''' Constructs the base query
        Args:
            view_kwargs (dict): kwargs from the resource view

        Returns:
            A query I presume.
        '''
        id_ = view_kwargs.get('id')
        type_ = view_kwargs.get('type_')
        query_ = self.session.query(self.model)

        if type_:
            model = get_class_by_tablename(type_[:-1])
            try:
                self.session.query(model).filter_by(id=id_).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {'parameter': 'id'}, "{}: {} not found".format(type_, id_))
            else:
                subq = self.session.query(model).filter(
                    model.id == id_).subquery()
                attr_name = self.attrs.get(type_, type_)
                query_ = query_.join(subq, attr_name, aliased=True)

        return query_

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
    def before_get(self, *args, **kwargs):
        print('really')

    def before_get_collection(self, qs, view_kwargs):
        print('before_get_collection', view_kwargs)
        print('qs dict', qs.__dict__)




    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post,
        'attrs': {
            'previews': 'preview',
            'images': 'image',
            'users': 'user'
        },
        'methods': {'query': BaseList.query,
            'before_get_collection': before_get_collection}
    }

class PostDetail(BaseDetail):
    def before_get_object(self, view_kwargs):
        type_ = view_kwargs.get('type_')
        if type_ and type_ not in ['comments', 'images', 'previews']:
            raise ObjectNotFound(
                {'parameter': 'post'}, "{} does not have attribute 'post'".format(type_))

    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post,
        'methods': {'before_get_object': before_get_object}
    }

class PostRelationship(BaseRelationship):
    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post,
    }

class PostRelationship(BaseRelationship):
    def before_patch(self, *args, **kwargs):
        print('before patch post', args, kwargs)

    def after_patch(self, result):
        print('after patch post', result)

    def before_create_relationship(self, json_data, relationship_field, related_id_field, view_kwargs):
        print('before update relationship')
        print('json_data', json_data, 'relationship_field',
              relationship_field, 'related_id_field', related_id_field, 'view_kwargs', view_kwargs)

    def after_update_relationship(self, obj, updated, json_data, relationship_field, related_id_field, view_kwargs):
        print('after update relationship')
        print(obj, updated, json_data, relationship_field,
              related_id_field, view_kwargs)

    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post,
        'eagerload_includes': False,
        'methods': {
            'before_create_relationship': before_create_relationship,
            'after_update_relationship': after_update_relationship
        }
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
    schema = schemas.TagSchema
    data_layer = {
        'session': db.session,
        'model': models.Tag,
        'eagerload_includes': False
    }

class TagDetail(BaseDetail):
    schema = schemas.TagSchema
    data_layer = {
        'session': db.session,
        'model': models.Tag
    }

class TagRelationship(BaseRelationship):
    def before_patch(self, *args, **kwargs):
        print('before patch tags', args, kwargs)

    def before_create_relationship(self, json_data, relationship_field, related_id_field, view_kwargs):
        print('before update relationship')
        print('json_data', json_data, 'relationship_field',
              relationship_field, 'related_id_field', related_id_field, 'view_kwargs', view_kwargs)

    schema = schemas.TagSchema
    data_layer = {
        'session': db.session,
        'model': models.Tag,
        'methods': {'before_create_relationship': before_create_relationship}
    }

class UserList(BaseList):
    def before_get(self, *args, **kwargs):
        print('really user')

    @processors.authenticate
    def before_post(self, *args, **kwargs):
        processors.remove_id(kwargs['data'])
        processors.username_preproc(kwargs['data'])


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
    attrs = {
        'posts': 'post',
        'users': 'user'
    }
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

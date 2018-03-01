# A smarter person than I could figure out how to generalize a lot of these methods

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

def split_type_id(view_kwargs):
    temp = {}
    for k, v in view_kwargs.items():
        splits = k.split('_')
        try:
            temp['type_'] = splits[0]
            temp['id'] = v
        except KeyError:
            pass
    try:
        view_kwargs['type_'] = temp['type_']
        view_kwargs['id'] = temp['id']
    except KeyError:
        pass

class BaseList(ResourceList):
    view_kwargs = True

    @processors.authenticate
    def before_post(self, *args, **kwargs):
        processors.remove_id(kwargs['data'])
        pass

    def before_get_collection(self, qs, view_kwargs):
        split_type_id(view_kwargs)

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
            query_ = model_query(self.session, model, id_, type_, self.attrs, query_)

        return query_

class BaseDetail(ResourceDetail):
    @processors.authenticate
    def before_patch(self, *args, **kwargs):
        pass

    @processors.authenticate
    def before_delete(self, *args, **kwargs):
        pass

    def after_get_object(self, obj, view_kwargs):
        if not obj:
            raise ObjectNotFound({'parameter': 'id'},
                                 "{}: {} not found".format(self.model.__tablename__, view_kwargs['id']))

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

def model_query(session, model, id_, type_, attrs, query_):
    try:
        session.query(model).filter_by(id=id_).one()
    except NoResultFound:
        raise ObjectNotFound(
            {'parameter': 'id'}, "{}: {} not found".format(type_, id_))
    else:
        subq = session.query(model).subquery()
        attr_name = attrs.get(type_, type_)

        query_ = query_.join(
            subq, attr_name, aliased=True).filter(model.id == id_)

    return query_

class PostList(BaseList):
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
            model = models.User if type_ == 'likes' else get_class_by_tablename(type_[:-1])
            query_ = model_query(self.session, model, id_, type_, self.attrs, query_)

        return query_

    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post,
        'attrs': {
            'previews': 'preview',
            'images': 'image',
            'users': 'user'
        },
        'methods':
        {
            'before_get_collection': BaseList.before_get_collection,
            'query': query
        }
    }

class PostDetail(BaseDetail):
    def before_get_object(self, view_kwargs):
        if view_kwargs.get('comments_id') is not None:
            try:
                comment = self.session.query(models.Comment).filter_by(
                    id=view_kwargs['comments_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'comments_id'},
                                     "Comment: {} not found".format(view_kwargs['comments_id']))
            else:
                if comment.post is not None:
                    view_kwargs['id'] = comment.post.id
                else:
                    view_kwargs['id'] = None

    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post,
        'methods': {
            'before_get_object': before_get_object,
            'after_get_object': BaseDetail.after_get_object
        }
    }

class PostRelationship(BaseRelationship):
    schema = schemas.PostSchema
    data_layer = {
        'session': db.session,
        'model': models.Post,
    }

class TagList(BaseList):
    schema = schemas.TagSchema
    data_layer = {
        'attrs': {},
        'session': db.session,
        'model': models.Tag,
        'methods':
        {
            'before_get_collection': BaseList.before_get_collection,
            'query': BaseList.query
        }
    }

class TagDetail(BaseDetail):
    schema = schemas.TagSchema
    data_layer = {
        'session': db.session,
        'model': models.Tag,
        'methods': {
            'after_get_object': BaseDetail.after_get_object
        }
    }

class TagRelationship(BaseRelationship):
    schema = schemas.TagSchema
    data_layer = {
        'session': db.session,
        'model': models.Tag,
    }

class UserList(BaseList):
    @processors.authenticate
    def before_post(self, *args, **kwargs):
        processors.remove_id(kwargs['data'])
        processors.username_preproc(kwargs['data'])

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
            model = models.Post if type_ == 'likes' else get_class_by_tablename(type_[:-1])
            query_ = model_query(self.session, model, id_, type_, self.attrs, query_)

        return query_


    schema = schemas.UserSchema
    data_layer = {
        'attrs': {},
        'session': db.session,
        'model': models.User,
        'methods': {
            'before_get_collection': BaseList.before_get_collection,
            'query': query,
        }
    }

class UserDetail(BaseDetail):
    def before_get_object(self, view_kwargs):
        if view_kwargs.get('comments_id') is not None:
            try:
                comment = self.session.query(models.Comment).filter_by(id=view_kwargs['comments_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'comments_id'},
                                     "Comment: {} not found".format(view_kwargs['comments_id']))
            else:
                if comment.user is not None:
                    view_kwargs['id'] = comment.user.id
                else:
                    view_kwargs['id'] = None

        if view_kwargs.get('posts_id') is not None:
            try:
                post = self.session.query(models.Comment).filter_by(
                    id=view_kwargs['posts_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'posts_id'},
                                     "Post: {} not found".format(view_kwargs['posts_id']))
            else:
                if post.user is not None:
                    view_kwargs['id'] = post.user.id
                else:
                    view_kwargs['id'] = None

    schema = schemas.UserSchema
    data_layer = {
        'session': db.session,
        'model': models.User,
        'methods': {
            'before_get_object': before_get_object,
            'after_get_object': BaseDetail.after_get_object
        }
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
        'model': models.Image,
        'methods': {'query': BaseList.query}
    }

class ImageDetail(BaseDetail):
    def before_get_object(self, view_kwargs):
        if view_kwargs.get('posts_id') is not None:
            try:
                image = self.session.query(models.Image).filter_by(
                    id=view_kwargs['posts_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'posts_id'},
                                     "Comment: {} not found".format(view_kwargs['posts_id']))
            else:
                if image.post is not None:
                    view_kwargs['id'] = image.post.id
                else:
                    view_kwargs['id'] = None

    schema = schemas.ImageSchema
    data_layer = {
        'session': db.session,
        'model': models.Image,
        'methods': {
            'before_get_object': before_get_object,
            'after_get_object': BaseDetail.after_get_object
        }
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
        'model': models.Preview,
        'methods': {'query': BaseList.query}
    }

class PreviewDetail(BaseDetail):
    def before_get_object(self, view_kwargs):
        if view_kwargs.get('posts_id') is not None:
            try:
                preview = self.session.query(models.Preview).filter_by(
                    id=view_kwargs['posts_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'posts_id'},
                                     "Comment: {} not found".format(view_kwargs['posts_id']))
            else:
                if preview.post is not None:
                    view_kwargs['id'] = preview.post.id
                else:
                    view_kwargs['id'] = None

    schema = schemas.PreviewSchema
    data_layer = {
        'session': db.session,
        'model': models.Preview,
        'methods': {
            'before_get_object': before_get_object,
            'after_get_object': BaseDetail.after_get_object
        }
    }

class PreviewRelationship(BaseRelationship):
    schema = schemas.PreviewSchema
    data_layer = {
        'session': db.session,
        'model': models.Preview
    }

class CommentList(BaseList):
    schema = schemas.CommentSchema
    data_layer = {
        'session': db.session,
        'model': models.Comment,
        'attrs': {
            'posts': 'post',
            'users': 'user'
        },
        'methods': {
            'before_get_collection': BaseList.before_get_collection,
            'query': BaseList.query
        }
    }

class CommentDetail(BaseDetail):
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
                subq = self.session.query(model).subquery()
                attr_name = self.attrs.get(type_, type_)
                query_ = query_.join(subq, attr_name, aliased=True).filter(model.id == id_)

        return query_

    schema = schemas.CommentSchema
    data_layer = {
        'session': db.session,
        'model': models.Comment,
        'methods': {'query': query}
    }

class CommentRelationship(BaseRelationship):
    schema = schemas.CommentSchema
    data_layer = {
        'session': db.session,
        'model': models.Comment
    }

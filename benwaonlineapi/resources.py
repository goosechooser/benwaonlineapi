from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship
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

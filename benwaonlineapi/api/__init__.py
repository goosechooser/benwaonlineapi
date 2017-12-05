"""
Package contains the API functionality for benwa.online
A JSONAPI is generated by flask-restless based on the models defined in models.py
processors.py contains pre and post-processors for all calls to the api
"""
from flask import Blueprint, request
from flask_restless import APIManager

# from benwaonlineapi.api import views, processors
from benwaonlineapi.api import processors, util

from benwaonlineapi.database import db
from benwaonlineapi import models

from marshmallow import pprint

api = Blueprint('api', __name__)

def remove_id(data, **kw):
    # Because marshmallow-jsonapi schemas REQUIRE id
    # and default flask-restless deserializer throws a shitfit
    # if theres a client generated id
    try:
        del data['data']['id']
    except KeyError:
        pass

global_preprocessors = {'POST_RESOURCE': [remove_id, processors.api_auth_func]}
                        # 'GET_COLLECTION': [processors.global_pre]}
                        # 'DELETE_RESOURCE': [check_authorization]}
user_preprocessors = {'POST_RESOURCE': [processors.username_preproc, processors.remove_token]}
# postprocessors = {'GET_TO_MANY_RELATION': [comments_post]}

manager = APIManager(flask_sqlalchemy_db=db, preprocessors=global_preprocessors)

comments_api = manager.create_api(models.Comment, collection_name='comments',
                                    methods=['GET', 'POST', 'DELETE', 'PATCH'])

users_api = manager.create_api(models.User, collection_name='users',
                                methods=['GET', 'POST', 'DELETE', 'PATCH'],
                                allow_to_many_replacement=True,
                                preprocessors=user_preprocessors)
                                # exclude=['user_id'])

posts_api = manager.create_api(models.Post, collection_name='posts',
                                methods=['GET', 'POST', 'PATCH'],
                                allow_to_many_replacement=True)

tags_api = manager.create_api(models.Tag, collection_name='tags',
                                methods=['GET', 'POST', 'PATCH'],
                                allow_to_many_replacement=True,
                                allow_functions=True)

images_api = manager.create_api(models.Image, collection_name='images',
                                methods=['GET', 'POST', 'PATCH'])

previews_api = manager.create_api(models.Preview, collection_name='previews',
                                  methods=['GET', 'POST', 'PATCH'])

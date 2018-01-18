"""
Package contains the API functionality for benwa.online
A JSONAPI is generated by flask-restless based on the models defined in models.py
processors.py contains pre and post-processors for all calls to the api
"""
import os
from flask import Blueprint, request
from flask_restless import APIManager

from benwaonlineapi.api import processors
from benwaonlineapi.database import db
from benwaonlineapi import models

api = Blueprint('api', __name__)
global_preprocessors = {
    'POST_RESOURCE': [processors.remove_id, processors.authenticate],
    'DELETE_RESOURCE': [processors.authenticate],
    'PATCH_RESOURCE': [processors.authenticate],
    'DELETE_RELATIONSHIP': [processors.authenticate],
    'POST_RELATIONSHIP': [processors.authenticate],
    'PATCH_RELATIONSHIP': [processors.authenticate]
}

global_preprocessors['GET_COLLECTION'] = [processors.cache_preprocessor]
global_postprocessors = {'GET_COLLECTION': [processors.cache_postprocessor]}

if os.getenv('FLASK_CONFIG') == 'test':
    global_preprocessors['GET_COLLECTION'].insert(0, processors.authenticate)

user_preprocessors = {'POST_RESOURCE': [processors.username_preproc]}
tag_postprocessors = {'GET_COLLECTION': [processors.count]}

manager = APIManager(
    flask_sqlalchemy_db=db,
    preprocessors=global_preprocessors,
    postprocessors=global_postprocessors)

comments_api = manager.create_api(models.Comment, collection_name='comments',
                                    methods=['GET', 'POST', 'DELETE', 'PATCH'],
                                    allow_to_many_replacement=True)

users_api = manager.create_api(models.User, collection_name='users',
                                methods=['GET', 'POST', 'DELETE', 'PATCH'],
                                allow_to_many_replacement=True,
                                preprocessors=user_preprocessors)

posts_api = manager.create_api(models.Post, collection_name='posts',
                                page_size=30,
                                methods=['GET', 'POST', 'PATCH'],
                                allow_to_many_replacement=True)

tags_api = manager.create_api(models.Tag, collection_name='tags',
                                methods=['GET', 'POST', 'PATCH'],
                                postprocessors=tag_postprocessors,
                                allow_to_many_replacement=True,
                                allow_functions=True)

images_api = manager.create_api(models.Image, collection_name='images',
                                methods=['GET', 'POST', 'PATCH'])

previews_api = manager.create_api(models.Preview, collection_name='previews',
                                  methods=['GET', 'POST', 'PATCH'])

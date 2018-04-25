import sys
import os
import json
import pytest

from benwaonlineapi import create_app
from benwaonlineapi import models
from benwaonlineapi.database import db as _db
from benwaonlineapi.cache import cache as _cache

sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))

@pytest.fixture(scope='session')
def jwks():
    with open('keys/test_jwks.json', 'r') as f:
        _jwks = json.load(f)

    yield _jwks

@pytest.fixture(scope='session')
def priv_key():
    fname = 'keys/benwaonline_api_test_priv.pem'
    with open(fname, 'r') as f:
        _priv_key = f.read()

    yield _priv_key

@pytest.fixture(scope='session')
def app():
    _app = create_app('test')

    with _app.app_context():
        yield _app

@pytest.fixture(scope='session')
def cache():
    yield _cache
    _cache.clear()

@pytest.fixture(scope='session')
def db(app):
    _db.app = app
    _db.create_all()

    yield _db

    _db.session.close_all()
    _db.drop_all()

@pytest.fixture(scope='function', autouse=True)
def db_session(db):
    connection = _db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = _db.create_scoped_session(options=options)
    _db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()

def setup_db(session):
    tag = init_tags(session)
    user = init_users(session)
    image = init_images(session)
    preview = init_previews(session)
    post = init_posts(session, user, image, preview, [tag])
    init_comments(session, user, post)

def init_tags(session):
    tag = models.Tag(name='benwa')
    session.add(tag)
    session.commit()
    return tag

def init_users(session):
    user = models.User(user_id='6969', username='Benwa Benwa Benwa')
    session.add(user)
    session.commit()
    return user

def init_images(session):
    image = models.Image(filepath='Benwa Benwa Benwa')
    session.add(image)
    session.commit()
    return image

def init_previews(session):
    preview = models.Preview(filepath='Benwa Benwa Benwa')
    session.add(preview)
    session.commit()
    return preview

def init_posts(session, user, image, preview, tags):
    post = models.Post(title='not null', user=user, image=image, preview=preview, tags=tags)
    session.add(post)
    user.posts.append(post)
    user.likes.append(post)
    session.commit()
    return post

def init_comments(session, user, post):
    comment = models.Comment(user=user, post=post, content='test comment')
    session.add(comment)
    session.commit()

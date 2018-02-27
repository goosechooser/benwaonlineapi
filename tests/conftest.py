import pytest

from benwaonlineapi import create_app
from benwaonlineapi import models
from benwaonlineapi.database import db as _db

@pytest.fixture(scope='session')
def app():
    app = create_app('test')

    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def db(app):
    _db.app = app
    _db.create_all()
    setup_db(_db.session)

    yield _db

    _db.session.close_all()
    _db.drop_all()

@pytest.fixture(scope='function')
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    db.session = session

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

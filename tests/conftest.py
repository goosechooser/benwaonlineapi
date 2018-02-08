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
    _db.drop_all()
    _db.create_all()
    init_tags(_db.session)

    yield _db

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

def init_tags(session):
    tag = models.Tag(name='benwa')
    session.add(tag)
    session.commit()

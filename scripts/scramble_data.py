'''Script to remove Tag entries that have the same name value but differing IDs.'''
from sqlalchemy import create_engine
from benwaonlineapi import models
from benwaonlineapi.database import db

from run import app


def connect():
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/')
    engine.execute('USE test_db')

    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    return session


def scramble(session):
    users = models.User.query.all()
    i = 0
    for u in users:
        u.user_id = 'scrambled-' + str(i)
        i += 1

if __name__ == '__main__':
    with app.app_context():
        connect()
        scramble(db.session)
        db.session.commit()

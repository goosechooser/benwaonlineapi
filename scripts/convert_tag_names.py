'''Script to convert existing Tag names entries into new tag name format
New format:
* all lowercase
* removes all '+', and '_' characters

Basically we'll run this, then run the 'remove_duplicate_tags' script
'''
from sqlalchemy import create_engine
from benwaonlineapi.models import Tag, Post
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

def convert(session):
    tags = Tag.query.all()
    print('old_tags', [tag.id for tag in tags])

    for tag in tags:
        converted = tag.name.lower().replace('+', ' ').replace('_', ' ')
        print(tag.name, '--->',converted)
        tag.name = converted

if __name__ == '__main__':
    with app.app_context():
        connect()
        convert(db.session)
        db.session.commit()

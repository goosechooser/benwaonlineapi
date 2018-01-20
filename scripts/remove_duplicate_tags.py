'''Script to remove Tag entries that have the same name value but differing IDs.'''
from sqlalchemy import create_engine
from benwaonlineapi.models import Tag, Post
from benwaonlineapi.database import db

from run import app

def connect():
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/')
    # 20$ says I run this on production
    engine.execute('USE test_db')

    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    return session
    # import benwaonlineapi.models
    # db.create_all()

def find_duplicates(session):
    memo = {}
    tags = Tag.query.all()
    print('old_tags', [tag.id for tag in tags])

    for tag in tags:
        memo[tag.name] = memo.get(tag.name, [])
        memo[tag.name].append(tag)

    duplicates = []
    for k, v in memo.items():
        if len(v) == 1:
            continue
        print(k, v, [(e.id, e.created_on) for e in v])
        duplicates.append({
            'oldest': v[0],
            'replace': v[1:]
        })
    return duplicates

def remove_duplicates(session, duplicates):
    print('\nREMOVING\n')
    posts = Post.query.all()
    for d in duplicates:
        for post in posts:
            tags = post.tags.order_by(Tag.created_on).all()
            if not set(d['replace']).isdisjoint(tags):
                print('old tags', [(tag.name, tag.id) for tag in tags])
                post.tags = [d['oldest'] if tag in d['replace'] else tag for tag in tags]

                tags = post.tags.order_by(Tag.created_on).all()
                print('new tags', [(tag.name, tag.id) for tag in tags])

                for r in d['replace']:
                    Tag.query.filter(Tag.id == r.id).delete(synchronize_session=False)
                session.commit()

def setup():
    with app.app_context():
        connect()
        duplicates = find_duplicates(db.session)
        remove_duplicates(db.session, duplicates)

if __name__ == '__main__':
        setup()


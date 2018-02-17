'''Script to remove Tag entries that have the same name value but differing IDs.'''
from sqlalchemy import create_engine
from benwaonlineapi.models import Tag, Post, posts_tags
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

def find_duplicates(session):
    memo = {}
    tags = Tag.query.all()
    # print('old_tags', [tag.id for tag in tags])

    for tag in tags:
        print('Tag name is', tag.name)
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
            tags = post.tags
            tags.sort(key=lambda tag: tag.created_on)
            if not set(d['replace']).isdisjoint(tags):
                print('old tags', [(tag.name, tag.id) for tag in tags])
                post.tags = [d['oldest'] if tag in d['replace'] else tag for tag in tags]

                # tags = post.tags.order_by(Tag.created_on).all()
                print('new tags', [(tag.name, tag.id) for tag in post.tags])

                for r in d['replace']:
                    print(r.name, r.id)
                    session.delete(Tag.query.get(r.id))
                    # Tag.query.filter(posts_tags.c.tags_id == r.id).delete(synchronize_session=False)

if __name__ == '__main__':
    with app.app_context():
        connect()
        duplicates = find_duplicates(db.session)
        remove_duplicates(db.session, duplicates)
        db.session.commit()


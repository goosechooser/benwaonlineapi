from sqlalchemy import create_engine
from benwaonlineapi.models import Tag, User
from benwaonlineapi.database import db

from run import app

def init_db():
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/')
    # 20$ says I run this on production
    engine.execute('DROP DATABASE benwaonline')
    engine.execute('CREATE DATABASE benwaonline')
    engine.execute('USE benwaonline')

    import benwaonlineapi.models
    db.create_all()

def init_tags(session):
    tag = Tag(name='benwa')
    session.add(tag)

    session.commit()

def init_users(session):
    user = User(username='TestBenwaExcellent', user_id='66666')
    session.add(user)

    session.commit()

def setup():
    with app.app_context():
        init_db()
        init_tags(db.session)

if __name__ == '__main__':
        setup()


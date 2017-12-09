from datetime import datetime, timedelta
from benwaonlineapi.database import db

posts_tags = db.Table('posts_tags',
                       db.Column('posts_id', db.Integer, db.ForeignKey('post.id')),
                       db.Column('tags_id', db.Integer, db.ForeignKey('tag.id')))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64))
    active = db.Column(db.Boolean(), default=True)
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User: {}>'.format(self.username)

class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Preview: {}>'.format(self.filepath)

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Image: {}>'.format(self.filepath)

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def owner_is(self, user):
        return user.id == self.user_id

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    image = db.relationship('Image', uselist=False, backref='post')
    preview = db.relationship('Preview', uselist=False, backref='post')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    tags = db.relationship('Tag', secondary=posts_tags, backref='posts', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return '<Tag: {}>'.format(self.name)

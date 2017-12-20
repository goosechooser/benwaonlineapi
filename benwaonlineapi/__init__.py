import os
from flask import Flask, g, url_for, request, flash, redirect, jsonify
from sqlalchemy import create_engine

from benwaonlineapi.config import app_config
from benwaonlineapi.database import db
from benwaonlineapi.api import api, manager
from benwaonlineapi.models import Tag, User

def create_app(config_name=None):
    """
    Returns the Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    db.init_app(app)
    manager.init_app(app)
    app.register_blueprint(api)

    @app.cli.command()
    def initdb():
        """Initialize the database."""
        init_db()
        init_tags(db.session)

    return app

def init_db():
    engine = create_engine(app.config['DB_BASE_URI'])
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

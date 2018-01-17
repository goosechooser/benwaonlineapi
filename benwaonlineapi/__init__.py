import os
import logging
from flask import Flask, g, url_for, request, flash, redirect, jsonify
from sqlalchemy import create_engine

from benwaonlineapi.config import app_config
from benwaonlineapi.database import db
from benwaonlineapi.api import api, manager
from benwaonlineapi import models

def setup_logger_handlers(loggers):
    fh = logging.FileHandler(__name__ +'_debug.log')
    fh.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    fh.setLevel(logging.DEBUG)
    for logger in loggers:
        logger.addHandler(fh)

    return

def create_app(config_name=None):
    """
    Returns the Flask app.
    """
    app = Flask(__name__)
    setup_logger_handlers([app.logger, logging.getLogger('gunicorn.error')])
    app.config.from_object(app_config[config_name])

    db.init_app(app)
    manager.init_app(app)
    app.register_blueprint(api)

    @app.cli.command()
    def initdb():
        """Initialize the database."""
        init_db(app)
        init_tags(db.session)

    return app

def init_db(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    # 20$ says I run this on production
    engine.execute('DROP DATABASE benwaonline')
    engine.execute('CREATE DATABASE benwaonline')
    engine.execute('USE benwaonline')

    import benwaonlineapi.models
    db.create_all()

def init_tags(session):
    tag = models.Tag(name='benwa')
    session.add(tag)

    session.commit()

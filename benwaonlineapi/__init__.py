import os
import logging
from flask import Flask, g, url_for, request, flash, redirect, jsonify
from sqlalchemy import create_engine

from benwaonlineapi.config import app_config
from benwaonlineapi.cache import cache
from benwaonlineapi.database import db, migrate
from benwaonlineapi.manager import manager
from benwaonlineapi import models

def setup_logger_handlers(app):
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
    ))
    sh.setLevel(logging.DEBUG)
    app.logger.addHandler(sh)

def create_app(config_name=None):
    """
    Returns the Flask app.
    """
    app = Flask(__name__)
    setup_logger_handlers(app)
    app.config.from_object(app_config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    manager.init_app(app)
    cache.init_app(app)

    @app.cli.command()
    def initdb():
        """Initialize the database."""
        init_db(app)
        init_tags(db.session)

    @app.cli.command()
    def routes():
        """List all the routes registered."""
        list_routes(app)

    return app

def init_db(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    # 20$ says I run this on production
    engine.execute('DROP DATABASE ' + app.config['DB_NAME'])
    engine.execute('CREATE DATABASE ' + app.config['DB_NAME'])
    engine.execute('USE ' + app.config['DB_NAME'])

    import benwaonlineapi.models
    db.create_all()

def init_tags(session):
    tag = models.Tag(name='benwa')
    session.add(tag)

    session.commit()

def list_routes(app):
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(
            rule.endpoint, methods, rule))
        output.append(line)

    for line in sorted(output):
        print(line)
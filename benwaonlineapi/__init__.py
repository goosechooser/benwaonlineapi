from flask import Flask, g, url_for, request, flash, redirect, jsonify
from config import app_config

from benwaonlineapi.database import db
from benwaonlineapi.api import api, manager

def create_app(config_name=None):
    """
    Returns the Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    db.init_app(app)
    manager.init_app(app)
    app.register_blueprint(api)

    return app

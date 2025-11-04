"""
Flask_API - Main Application.

Flask_API is a boilerplate/template for Flask REST API applications.
This application is built with Flask and follows a modular architecture using Blueprints, ensuring scalability and maintainability.

This file contains functions to initialize Flask and Database.
You shouldn't have to change those functions except for advance functionality.

"""
import logging

from flask import Flask
from flask_apscheduler import APScheduler

from Flask_API.blueprints import register_blueprints
from Flask_API.db import db


def create_app(config_filename: str = None) -> Flask:
    """
    Create Flask App.

    Flask Application Factory Pattern. Creating the Flask App in a function
    makes instancing of the app possible for testing or multi-configuration.
    create_app() is recognized by the `flask run` command.

    documentation :
    https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/#basic-factories

    :param config_filename: path to the config file name. If None, default
                            `config/settings.py` is loaded
    :type config_filename: str
    :return: Flask App object
    :rtype: Flask
    """
    #: Instanciate a Flask App with the name of the service
    app = Flask(__name__)
    #: Load Flask Configuration
    #:
    #: By Default the application will load `config/settings.py` for developement.
    #: You can pass a python configuration file path as parameter of this function.

    if config_filename:
        app.config.from_pyfile(config_filename)
    else:
       app.config.from_object('Flask_API.config.settings-dev')

    #: Init the project database
    db.init_app(app)

    #: Import models module to create the tables in the database if the database.db file doesn't exist
    import Flask_API.models  # noqa
    with app.app_context():
        db.create_all()  # Make sure this call is done when in app_context
        scheduler = APScheduler()
        scheduler.init_app(app)
        app.scheduler = scheduler

    #: Register Blueprints
    #:
    #: Every Blueprints to load must be added to the following function
    #: being at blueprints/__init__.py
    register_blueprints(app)

    log_file_path = app.config.get("LOG_FILE")
    file_handler = logging.FileHandler(log_file_path)
    app.logger.addHandler(file_handler)
    app.scheduler.start()
    return app

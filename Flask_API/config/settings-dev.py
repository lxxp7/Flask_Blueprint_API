"""
Flask Configuration Dev Mode.

This is a Flask Configuration
It holds all configuration parameters for the Flask App.
"""

import os

# -----------------------------------------------------------------------------
# Flask Configuration
#
# https://flask.palletsprojects.com/en/1.1.x/config/#builtin-configuration-values
# -----------------------------------------------------------------------------
ENV = "development"
DEBUG = True
# TEMPLATES_AUTO_RELOAD = True

# URI configuration for the SQLite DB
# Absolute path to app base directory
rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
db_path = "sqlite:///" + os.path.join(rootdir, "database.db")

# Flask App host and port
FLASK_HOST = os.environ.get("FLASK_HOST", "127.0.0.1")
FLASK_PORT = os.environ.get("FLASK_PORT", "5000")
# Database URI
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", db_path)

# Logging file paths
LOG_FILE = os.environ.get("LOG_FILE", "logs/FlaskAPI.log")
ERRORS_LOG_FILE = os.environ.get("ERRORS_LOG_FILE", "logs/errors.log")
WARNINGS_LOG_FILE = os.environ.get("WARNINGS_LOG_FILE", "logs/warnings.log")
INFO_LOG_FILE = os.environ.get("INFO_LOG_FILE", "logs/info.log")

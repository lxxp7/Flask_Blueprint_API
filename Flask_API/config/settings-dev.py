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
rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_path = 'sqlite:///' + os.path.join(rootdir, 'database.db')

FLASK_HOST = "127.0.0.1"
FLASK_PORT = "5000"
SQLALCHEMY_DATABASE_URI = db_path
LOG_FILE = "app_logs.log"
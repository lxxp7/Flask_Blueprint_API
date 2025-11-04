"""
Flask Configuration Production Mode.

This is a Flask Configuration
It holds all configuration parameters for the Flask App
"""
import os

# -----------------------------------------------------------------------------
# Flask Configuration
#
# https://flask.palletsprojects.com/en/1.1.x/config/#builtin-configuration-values
# -----------------------------------------------------------------------------

ENV = "production"

# URI configuration for the SQLite DB
# Absolute path to app base directory
rootdir = 'path/to/app/database/directory'
db_path = 'database_to_use:///'+ os.path.join(rootdir, 'database_name.db')

# Flask App settings for production
FLASK_HOST = "public_ip_address"
FLASK_PORT = "public_port"
SQLALCHEMY_DATABASE_URI = db_path
LOG_FILE = "path/to/app/logs/app_logs.log"

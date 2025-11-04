"""Initialization file for the app db, moved from Flask_API/__init__ to avoid circular import."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

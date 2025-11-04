"""Initialization file for the app db, moved from FlaskBlueprintTemplateApp/__init__ to avoid circular import."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""
This module defines the database models for the Flask application.

It contains SQLAlchemy models representing database tables.
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from Flask_API import db


class Table(db.Model):
    """
    Represents a generic table.
    """

    __tablename__ = 'Table'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(String(512), nullable=True)
    is_active = Column(Boolean, default=True)


class RelatedTable(db.Model):
    """
    Represents a table related to the Table model.
    """

    __tablename__ = 'RelatedTable'
    id = Column(Integer, primary_key=True)
    table_id = Column(Integer, ForeignKey('Table.id'), nullable=False)
    info = Column(String(256), nullable=False)

    table = relationship('Table', backref=backref('related_tables', lazy=True))
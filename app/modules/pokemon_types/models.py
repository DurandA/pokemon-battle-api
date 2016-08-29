# encoding: utf-8
"""
Pokemon types database models
--------------------
"""
from sqlalchemy_utils import types as column_types, Timestamp
from sqlalchemy.ext.automap import automap_base
from flask_sqlalchemy import BaseQuery

from app.extensions import db


class PokemonType(db.Model):
    """
    Pokemon type database model.
    """
    __tablename__ = 'types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('identifier', db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return (
            "<{class_name}("
            "id={self.id}, "
            "name=\"{self.name}\""
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )

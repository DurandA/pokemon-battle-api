# encoding: utf-8
"""
Player database models
--------------------
"""
from sqlalchemy_utils import types as column_types, Timestamp
from sqlalchemy.ext.automap import automap_base
from flask_sqlalchemy import BaseQuery

from app.extensions import db
from app.modules.pokemon_types.models import PokemonType


types = db.Table('pokemon_types', db.metadata,
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id')),
    db.Column('type_id', db.Integer, db.ForeignKey('types.id'))
)


class Pokemon(db.Model):
    """
    Pokemon database model.
    """
    __tablename__ = 'pokemon'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('identifier', db.String(30), nullable=False, unique=True)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    types = db.relationship(PokemonType, secondary=types,
                             backref=db.backref('pokemons', lazy='dynamic'))

    def __repr__(self):
        return (
            "<{class_name}("
            "id={self.id}, "
            "name=\"{self.name}\", "
            "height=\"{self.height}\", "
            "weight=\"{self.weight}\""
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )



# tables = ['pokemon', 'types']#'pokemon_types']
# db.metadata.reflect(db.engine, only=tables)
# Base = automap_base(metadata=db.metadata)
# Base.prepare()
# db.register_base(Base)
# Pokemon = Base.classes.pokemon
# PokemonType = Base.classes.types

#Base.query = db.session.query_property()

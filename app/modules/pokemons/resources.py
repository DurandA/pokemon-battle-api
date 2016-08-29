# encoding: utf-8
# pylint: disable=too-few-public-methods,invalid-name
"""
RESTful API Pokemon resources
--------------------------
"""

import logging

from flask_login import current_user
from flask_restplus import Resource
import sqlalchemy

from app.extensions import db
from app.extensions.api import Namespace, abort, http_exceptions
from app.extensions.api.parameters import PaginationParameters

from . import parameters, schemas
from .models import Pokemon#, PokemonType


log = logging.getLogger(__name__)
api = Namespace('pokemons', description="Pokemons")


@api.route('/')
class Pokemons(Resource):
    """
    Manipulations with sports.
    """

    @api.response(schemas.BasePokemonSchema(many=True))
    def get(self):
        """
        List of pokemons.

        Returns a list of pokemons starting from ``offset`` limited by ``limit``
        parameter.
        """
        return Pokemon.query
        for pokemon in db.session.query(Pokemon):
            print(pokemon.identifier)
            #print(pokemon.pokemon_types_collection)
            print(pokemon.types_collection)
        return db.session.query(Pokemon)


@api.route('/<int:pokemon_id>')
@api.response(
    code=http_exceptions.NotFound.code,
    description="Pokemon not found.",
)
class PokemonByID(Resource):
    """
    Manipulations with a specific pokemon.
    """

    @api.resolve_object_by_model(Pokemon, 'pokemon')
    @api.response(schemas.DetailedPokemonSchema())
    def get(self, pokemon):

        """
        Get pokemon details by ID.
        """
        return pokemon

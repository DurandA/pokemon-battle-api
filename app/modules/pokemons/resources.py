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

    #@api.parameters(PaginationParameters())
    @api.parameters(parameters.PokemonsParameters())
    @api.response(schemas.BasePokemonSchema(many=True))
    def get(self, args):
        """
        List of pokemons.

        Returns a list of pokemons starting from ``offset`` limited by ``limit``
        parameter.
        """
        q = Pokemon.query
        if 'pokemon_type' in args:
            q = q.filter(Pokemon.types.any(id=args['pokemon_type']))
            #q = q.filter_by(pokemon_type_id=args['pokemon_type'])
        return q.offset(args['offset']).limit(args['limit'])


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

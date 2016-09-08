# encoding: utf-8
# pylint: disable=too-few-public-methods,invalid-name
"""
RESTful API Sport resources
--------------------------
"""

import logging

import sqlalchemy
from flask_login import current_user
from flask_restplus import Resource

from app.extensions.api import Namespace, abort, http_exceptions
from app.extensions.api.parameters import PaginationParameters

from . import schemas
from .models import PokemonType

log = logging.getLogger(__name__)
api = Namespace('pokemon-types', description="Pokemon Types")



@api.route('/')
class PokemonTypes(Resource):
    """
    Manipulations with pokemon types.
    """

    @api.parameters(PaginationParameters())
    @api.response(schemas.PokemonTypeSchema(many=True))
    def get(self, args):
        """
        List of pokemon types.

        Returns a list of pokemon types starting from ``offset`` limited by ``limit``
        parameter.
        """
        return PokemonType.query.offset(args['offset']).limit(args['limit'])



# @api.route('/helloworld')
# class Hellworld(Resource):
#     """
#     Hello world.
#     """
#
#     def get(self):
#         """
#         Hello world.
#         """
#         return {"recaptcha_server_key": "TODO"}

from marshmallow import validate

from flask_marshmallow import base_fields
from flask_restplus_patched import Parameters

from app.extensions.api.parameters import PaginationParameters


class PokemonsParameters(PaginationParameters):
    """
    Helper Parameters class to reuse pagination.
    """

    pokemon_type = base_fields.Integer(
        description="pokemon type ID"
    )

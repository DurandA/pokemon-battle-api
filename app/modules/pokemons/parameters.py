from marshmallow import validate

from flask_marshmallow import base_fields
from flask_restplus_patched import Parameters

from app.extensions.api.parameters import PaginationParameters


class JSONParameters(Parameters):
    my_int = base_fields.Integer(
        description="pokemon type ID"
    )

class PokemonsParameters(PaginationParameters):
    """
    Helper Parameters class to reuse pagination.
    """

    pokemon_type = base_fields.Integer(
        description="pokemon type ID"
    )
    payload = base_fields.Nested(
        JSONParameters,
        exclude=(),
        location='json',
    )

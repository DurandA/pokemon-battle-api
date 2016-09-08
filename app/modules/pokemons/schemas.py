# encoding: utf-8
"""
Serialization schemas for Pokemon resources RESTful API
----------------------------------------------------
"""

from flask_marshmallow import base_fields
from flask_marshmallow import base_fields
from flask_restplus_patched import ModelSchema

from app.modules.users.schemas import BaseUserSchema
from app.modules.pokemon_types.schemas import PokemonTypeSchema

from .models import Pokemon, PokemonType


class BasePokemonSchema(ModelSchema):
    """
    Base pokemon schema exposes only the most general fields.
    """

    class Meta:
        # pylint: disable=missing-docstring
        model = Pokemon
        fields = (
            Pokemon.id.key,
            Pokemon.name.key,
        )


class DetailedPokemonSchema(BasePokemonSchema):
    """
    Detailed pokemon schema exposes all useful fields.
    """

    types = base_fields.Nested(
        'PokemonTypeSchema',
        exclude=(),
        many=True
    )

    class Meta(BasePokemonSchema.Meta):
        fields = BasePokemonSchema.Meta.fields + (
            Pokemon.height.key,
            Pokemon.weight.key,
            Pokemon.types.key,
        )

# encoding: utf-8
"""
Serialization schemas for Pokemon resources RESTful API
----------------------------------------------------
"""

from flask_marshmallow import base_fields
from flask_restplus_patched import ModelSchema

from .models import PokemonType


class PokemonTypeSchema(ModelSchema):

    class Meta:
        model = PokemonType
        fields = (
            PokemonType.id.key,
            PokemonType.name.key,
        )

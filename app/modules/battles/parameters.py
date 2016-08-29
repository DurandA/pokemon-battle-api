# encoding: utf-8
"""
Input arguments (Parameters) for Battle resources RESTful API
-----------------------------------------------------------
"""

from flask_marshmallow import base_fields
from flask_restplus_patched import Parameters, PostFormParameters, PatchJSONParameters

from . import schemas
from .models import Battle



class OpponentParameters(PostFormParameters):
    team_num = base_fields.Integer(description="[1-2] (one of both teams)", required=True, location='header')
    team_num.metadata['location'] = 'form'


class PokemonParameters(PostFormParameters):
    pokemon_id = base_fields.Integer(required=True)


class CreateBattleParameters(PostFormParameters):
    trainer1_id = base_fields.Integer(required=True)
    trainer2_id = base_fields.Integer(required=True)
    opponent1_pokemons = base_fields.List(base_fields.Integer, required=True)
    opponent2_pokemons = base_fields.List(base_fields.Integer, required=True)
    #opponent2_pokemons = base_fields.Nested(PokemonParameters, many=True, required=True)

    start_time = base_fields.DateTime(required=True)
    lat = base_fields.Float()
    lng = base_fields.Float()


class AddBattleParameters(PostFormParameters):
    player_id = base_fields.Integer(required=True)
    team_id = base_fields.Integer(required=True)
    timestamp = base_fields.DateTime(required=False)


class LocationParameters(PostFormParameters):
    lat = base_fields.Float(required=True)
    lng = base_fields.Float(required=True)

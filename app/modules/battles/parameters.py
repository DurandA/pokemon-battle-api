# encoding: utf-8
"""
Input arguments (Parameters) for Battle resources RESTful API
-----------------------------------------------------------
"""

from flask_marshmallow import base_fields
from flask_restplus_patched import Parameters, PostFormParameters, PatchJSONParameters, fields, reqparse, Model

from . import schemas, ns
from .models import Battle


class TeamNumParameters(PostFormParameters):
    team_num = base_fields.Integer(description="[1-2] (one of both teams)", required=True, location='header')
    team_num.metadata['location'] = 'form'


class PokemonParameters(PostFormParameters):
    pokemon_id = base_fields.Integer(required=True)


TeamParameters = ns.model('BattleTeam', {
    'trainer_id': fields.Integer(required=True),
    'pokemon_ids': fields.List(fields.Integer, required=True),
})


LocationParameters = ns.model('BattleLocation', {
    'lat': fields.Float(required=True),
    'lng': fields.Float(required=True),
})


CreateBattleParameters = ns.model('Battle', {
    'team1': fields.Nested(TeamParameters),
    'team2': fields.Nested(TeamParameters),
    'start_time': fields.DateTime(required=True),
    'location': fields.Nested(LocationParameters),
})


class OutcomeParameters(Parameters):
    trainer_id = base_fields.Integer(required=True)


outcome_parser = reqparse.RequestParser()
outcome_parser.add_argument('trainer', type=str, required=True)

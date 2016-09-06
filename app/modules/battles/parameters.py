# encoding: utf-8
"""
Input arguments (Parameters) for Battle resources RESTful API
-----------------------------------------------------------
"""

from marshmallow import validates, ValidationError
from flask_marshmallow import base_fields
from flask_restplus_patched import Parameters, PostFormParameters, PatchJSONParameters, fields, reqparse, Model

from . import schemas, ns
from .models import Battle

from app.extensions.api.parameters import PaginationParameters


class BattleParameters(PaginationParameters):
    is_finished = base_fields.Boolean(required=False)


class TeamNumParameters(PostFormParameters):
    team_num = base_fields.Integer(description="[1-2] (one of both teams)", required=True, location='header')
    team_num.metadata['location'] = 'form'


class LocationParameters(Parameters, schemas.LocationSchema):
    pass


class CreateBattleParameters(Parameters, schemas.CreateBattleSchema):

    class Meta:
        fields = schemas.CreateBattleSchema.Meta.fields

    @validates('team1')
    @validates('team2')
    def validate_pokemons(self, data):
        try:
            if 1 <= len(data['pokemon_ids']) <= 6:
                return
        except KeyError:
            pass
        raise ValidationError('Each team should have between 1 and 6 pokemons!')


class OutcomeParameters(Parameters):
    trainer_id = base_fields.Integer(required=True, location='json')


outcome_parser = reqparse.RequestParser()
outcome_parser.add_argument('trainer', type=str, required=True)

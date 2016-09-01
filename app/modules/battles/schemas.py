# encoding: utf-8
"""
Serialization schemas for Match resources RESTful API
----------------------------------------------------
"""

from marshmallow import post_load
from flask_marshmallow import base_fields
from flask_restplus_patched import ModelSchema, Schema
from marshmallow_sqlalchemy import property2field, field_for, fields

from .models import Battle, Location, Team#, Point
from app.modules.pokemons.schemas import BasePokemonSchema
from app.modules.pokemons.models import Pokemon
from app.modules.trainers.models import Trainer


import datetime


class LocationSchema(ModelSchema):
    """
    Location schema exposes all useful fields.
    """

    class Meta:
        model = Location
        fields = (
            Location.lat.key,
            Location.lng.key,
        )


class TeamBattleAPISchema(Schema):
    trainer = base_fields.Function(lambda obj: obj.trainer.name)
    pokemon = base_fields.Function(lambda obj: [p.id for p in obj.pokemons])


class BattleAPISchema(Schema):
    team1 = base_fields.Nested(
        'TeamBattleAPISchema',
        exclude=(),
    )
    team2 = base_fields.Nested(
        'TeamBattleAPISchema',
        exclude=(),
    )


class BaseBattleSchema(ModelSchema):
    """
    Base battle schema exposes only the most general fields.
    """

    team1 = base_fields.Nested(
        'TeamSchema',
        exclude=(),
    )
    team2 = base_fields.Nested(
        'TeamSchema',
        exclude=(),
    )
    #is_finished = base_fields.Method("get_is_finished")
    end_time = base_fields.Function(lambda obj: obj.updated if obj.winner else None)

    # def get_is_finished(self, obj):
    #     return datetime.datetime.now() > obj.start_time + datetime.timedelta(minutes = 90)

    #field_for(Match, 'start_time', dump_only=True)

    class Meta:
        # pylint: disable=missing-docstring
        model = Battle
        fields = (
            Battle.id.key,
            Battle.team1.key,
            Battle.team2.key,
            Battle.start_time.key,
            'end_time',
            #'is_finished',
        )
        dump_only = (
            Battle.id.key,
            'end_time',
        )


class TeamSchema(ModelSchema):
    trainer = base_fields.Nested(
        'BaseTrainerSchema',
        exclude=(),
    )
    pokemons = base_fields.Nested(
        BasePokemonSchema,
        exclude=(),
        many=True,
    )

    class Meta:
        # pylint: disable=missing-docstring
        model = Team
        fields = (
            Team.trainer.key,
            Team.pokemons.key,
        )
        dump_only = (
            Team.trainer.key,
        )


class DetailedBattleSchema(BaseBattleSchema):
    """
    Detailed battle schema exposes all useful fields.
    """
    # members = base_fields.Nested(
    #     'BaseTeamMemberSchema',
    #     exclude=(TeamMember.team.key, ),
    #     many=True
    # )
    location = base_fields.Nested(
        'LocationSchema',
        exclude=(),
    )
    team1 = base_fields.Nested(
        'TeamSchema',
        exclude=(),
    )
    team2 = base_fields.Nested(
        'TeamSchema',
        exclude=(),
    )

    class Meta(BaseBattleSchema.Meta):
        fields = BaseBattleSchema.Meta.fields + (
            Battle.location.key,
            Battle.team1.key,
            Battle.team2.key,
        )


class CreateTeamSchema(Schema):
    trainer_id = base_fields.Integer(required=True),
    pokemon_ids = base_fields.List(base_fields.Integer, required=True),

    class Meta:
        fields = (
            'trainer_id',
            'pokemon_ids',
        )


class CreateBattleSchema(Schema):
    location = base_fields.Nested(LocationSchema)
    team1 = base_fields.Nested(CreateTeamSchema, required=True)
    team2 = base_fields.Nested(CreateTeamSchema, required=True)
    start_time = base_fields.DateTime(required=True)

    @post_load
    def make_battle(self, data):
        for tkey, t in [(tk, data.pop(tk)) for tk in ('team1', 'team2')]:
            data[tkey] = team = Team(trainer_id=t["trainer_id"])
            for pokemon_id in t['pokemon_ids']:
                p = Pokemon.query.get(pokemon_id)
                team.pokemons.append(p)

        return Battle(**data)

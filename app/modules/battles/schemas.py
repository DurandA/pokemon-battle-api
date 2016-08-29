# encoding: utf-8
"""
Serialization schemas for Match resources RESTful API
----------------------------------------------------
"""

from flask_marshmallow import base_fields
from flask_restplus_patched import ModelSchema
from marshmallow_sqlalchemy import property2field, field_for, fields

from .models import Battle, Location, Opponent#, Point

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

class BaseBattleSchema(ModelSchema):
    """
    Base battle schema exposes only the most general fields.
    """

    team1 = base_fields.Nested(
        'BaseTrainerSchema',
        exclude=(),
    )
    team2 = base_fields.Nested(
        'BaseTrainerSchema',
        exclude=(),
    )
    is_finished = base_fields.Method("get_is_finished")

    def get_is_finished(self, obj):
        return datetime.datetime.now() > obj.start_time + datetime.timedelta(minutes = 90)

    #field_for(Match, 'start_time', dump_only=True)
    #start_time = fields.Str()

    class Meta:
        # pylint: disable=missing-docstring
        model = Battle
        fields = (
            Battle.id.key,
            Battle.opponent1.key,
            Battle.opponent2.key,
            Battle.start_time.key,
            'is_finished',
            #'is_finished',
        )
        dump_only = (
            Battle.id.key,
            #'is_finished',
        )


class OpponentSchema(ModelSchema):
    trainer = base_fields.Nested(
        'BaseTrainerSchema',
        exclude=(),
    )
    pokemons = base_fields.Nested(
        'BasePokemonSchema',
        exclude=(),
        many=True,
    )

    class Meta:
        # pylint: disable=missing-docstring
        model = Opponent
        fields = (
            Opponent.trainer.key,
            Opponent.pokemons.key,
        )
        dump_only = (
            Opponent.trainer.key,
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
    opponent1 = base_fields.Nested(
        'OpponentSchema',
        exclude=(),
    )
    opponent2 = base_fields.Nested(
        'OpponentSchema',
        exclude=(),
    )

    class Meta(BaseBattleSchema.Meta):
        fields = BaseBattleSchema.Meta.fields + (
            Battle.location.key,
            Battle.opponent1.key,
            Battle.opponent2.key,
        )


# class PointSchema(ModelSchema):
#     """
#     Point schema exposes all useful fields.
#     """
#
#     player = base_fields.Nested(
#         'BasePlayerSchema',
#         exclude=()
#     )
#
#     class Meta:
#         model = Point
#         fields = (
#             Point.team.key,
#             Point.player.key,
#             Point.timestamp.key,
#             Point.value.key,
#         )
#         dump_only = (
#             Point.team.key,
#             Point.player.key,
#         )

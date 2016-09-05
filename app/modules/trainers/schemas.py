# encoding: utf-8
"""
Serialization schemas for Team resources RESTful API
----------------------------------------------------
"""

from flask_marshmallow import base_fields
from flask_restplus_patched import ModelSchema

from app.modules.users.schemas import BaseUserSchema

from .models import Trainer#, TeamMember


class BaseTrainerSchema(ModelSchema):
    """
    Base trainer schema exposes only the most general fields.
    """

    class Meta:
        # pylint: disable=missing-docstring
        model = Trainer
        fields = (
            Trainer.id.key,
            Trainer.name.key,
            Trainer.gender.key,
            Trainer.country_code.key,
        )
        dump_only = (
            Trainer.id.key,
        )


class DetailedTrainerSchema(BaseTrainerSchema):
    """
    Detailed trainer schema exposes all useful fields.
    """

    # members = base_fields.Nested(
    #     'BaseTeamMemberSchema',
    #     exclude=(TeamMember.team.key, ),
    #     many=True
    # )

    class Meta(BaseTrainerSchema.Meta):
        fields = BaseTrainerSchema.Meta.fields + (
            Trainer.gender.key,
            Trainer.created.key,
            Trainer.updated.key,
        )


# class BaseTeamMemberSchema(ModelSchema):
#
#     team = base_fields.Nested(BaseTeamSchema)
#     player = base_fields.Nested(BaseUserSchema)
#
#     class Meta:
#         model = TeamMember
#         fields = (
#             TeamMember.team.key,
#             TeamMember.player.key,
#             TeamMember.is_leader.key,
#         )

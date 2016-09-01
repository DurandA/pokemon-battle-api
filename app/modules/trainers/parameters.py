# encoding: utf-8
"""
Input arguments (Parameters) for Trainer resources RESTful API
-----------------------------------------------------------
"""

from flask_marshmallow import base_fields
from flask_restplus_patched import PostFormParameters, PatchJSONParameters

from . import schemas
from .models import Trainer


class CreateTrainerParameters(PostFormParameters, schemas.BaseTrainerSchema):

    class Meta(schemas.BaseTrainerSchema.Meta):
        # This is not supported yet: https://github.com/marshmallow-code/marshmallow/issues/344
        required = (
            Trainer.name.key,
            Trainer.gender.key,
        )


class PatchTrainerDetailsParameters(PatchJSONParameters):
    # pylint: disable=missing-docstring
    OPERATION_CHOICES = (
        PatchJSONParameters.OP_REPLACE,
    )

    PATH_CHOICES = tuple(
        '/%s' % field for field in (
            Trainer.name.key,
        )
    )


# class AddTeamMemberParameters(PostFormParameters):
#     player_id = base_fields.Integer(required=True)
#     is_leader = base_fields.Boolean(required=False)

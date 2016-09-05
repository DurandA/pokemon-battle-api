# encoding: utf-8
"""
Input arguments (Parameters) for Trainer resources RESTful API
-----------------------------------------------------------
"""
from six import itervalues
from flask_marshmallow import base_fields
from flask_restplus_patched import Parameters, PostFormParameters, PatchJSONParameters, fields

from . import schemas, ns
from .models import Trainer


class CreateTrainerParameters(Parameters, schemas.BaseTrainerSchema):


    class Meta(schemas.BaseTrainerSchema.Meta):
        # This is not supported yet: https://github.com/marshmallow-code/marshmallow/issues/344
        required = (
            Trainer.name.key,
            Trainer.gender.key,
        )


CreateTrainerParameters = ns.model('Battle', {
    'name': fields.String(required=True),
    'gender': fields.String(required=True, enum=['male', 'female']),
    'country_code': fields.String(min_length=2, max_length=3),
})


class PatchTrainerDetailsParameters(PatchJSONParameters):
    # pylint: disable=missing-docstring
    OPERATION_CHOICES = (
        PatchJSONParameters.OP_REPLACE,
    )

    PATH_CHOICES = tuple(
        '/%s' % field for field in (
            Trainer.name.key,
            Trainer.gender.key,
        )
    )


# class AddTeamMemberParameters(PostFormParameters):
#     player_id = base_fields.Integer(required=True)
#     is_leader = base_fields.Boolean(required=False)

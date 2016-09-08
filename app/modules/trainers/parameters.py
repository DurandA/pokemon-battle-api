# encoding: utf-8
"""
Input arguments (Parameters) for Trainer resources RESTful API
-----------------------------------------------------------
"""
from flask_marshmallow import base_fields
from iso3166 import countries
from marshmallow import ValidationError, validates
from six import itervalues

from flask_restplus_patched import (Parameters, PatchJSONParameters,
                                    PostFormParameters, fields)

from . import ns, schemas
from .models import Trainer


# class CreateTrainerParameters(Parameters, schemas.BaseTrainerSchema):
#
#
#     class Meta(schemas.BaseTrainerSchema.Meta):
#         # This is not supported yet: https://github.com/marshmallow-code/marshmallow/issues/344
#         required = (
#             Trainer.name.key,
#             Trainer.gender.key,
#         )


class CreateTrainerParameters(Parameters, schemas.BaseTrainerSchema):
    # name = base_fields.String(required=True)
    # gender = base_fields.String(required=True, enum=['male', 'female'])
    # country_code = base_fields.String(min_length=2, max_length=3)
    class Meta:
        fields = (
            Trainer.name.key,
            Trainer.gender.key,
            Trainer.country_code.key,
        )

    @validates('name')
    def validate_name(self, data):
        if data != data.strip():
            raise ValidationError('Should not begin or end with whitespace!')
        if len(data)<3:
            raise ValidationError('Too short!')
        if not data.istitle():
            raise ValidationError('Should be titlecased!')

    @validates('country_code')
    def validate_country_code(self, data):
        try:
            countries.get(data)
        except KeyError:
            raise ValidationError('Should be an iso3166 country code!')


class PatchTrainerDetailsParameters(PatchJSONParameters):
    # pylint: disable=missing-docstring
    OPERATION_CHOICES = (
        PatchJSONParameters.OP_REPLACE,
    )

    PATH_CHOICES = tuple(
        '/%s' % field for field in (
            Trainer.name.key,
            Trainer.gender.key,
            Trainer.country_code.key,
        )
    )

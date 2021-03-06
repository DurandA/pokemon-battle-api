# encoding: utf-8
"""
RESTful API Trainer resources
--------------------------
"""

import logging

import sqlalchemy
from flask import request
from flask_restplus import Resource

from app.extensions import db, limiter
from app.extensions.api import api_v1 as api
from app.extensions.api import Namespace, abort, http_exceptions
from app.extensions.api.parameters import PaginationParameters
from app.modules.battles.models import Team

from . import ns, parameters, schemas
from .models import Trainer  # , TeamMember

log = logging.getLogger(__name__) # pylint: disable=invalid-name


@ns.route('/')
class Trainers(Resource):
    """
    Manipulations with trainers.
    """
    decorators = [limiter.limit("5/minute;50/hour", exempt_when=lambda: 'localhost' in request.headers['Host'], methods=('post',), per_method=True, error_message='Enhance your calm.')]

    @ns.parameters(PaginationParameters())
    @ns.response(schemas.BaseTrainerSchema(many=True))
    def get(self, args):
        """
        List of trainers.

        Returns a list of trainers starting from ``offset`` limited by ``limit``
        parameter.
        """
        return Trainer.query.offset(args['offset']).limit(args['limit'])

    #@ns.expect(parameters.CreateTrainerParameters)
    @ns.parameters(parameters.CreateTrainerParameters(), locations=('json',))
    @ns.response(schemas.DetailedTrainerSchema())
    @ns.response(code=http_exceptions.Conflict.code)
    def post(self, trainer_data):
        """
        Create a new trainer.
        """
        try:
            try:
                trainer = Trainer(**trainer_data)
            except ValueError as exception:
                abort(code=http_exceptions.Conflict.code, message=str(exception))
            db.session.add(trainer)
            try:
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                abort(code=http_exceptions.Conflict.code, message="Could not create a new trainer.")
        finally:
            db.session.rollback()
        return trainer


@ns.route('/<int:trainer_id>')
@ns.response(
    code=http_exceptions.NotFound.code,
    description="Trainer not found.",
)
class TrainerByID(Resource):
    """
    Manipulations with a specific trainer.
    """

    @ns.resolve_object_by_model(Trainer, 'trainer')
    @ns.response(schemas.DetailedTrainerSchema())
    def get(self, trainer):
        """
        Get trainer details by ID.
        """
        return trainer

    @ns.resolve_object_by_model(Trainer, 'trainer')
    @ns.parameters(parameters.PatchTrainerDetailsParameters())
    @ns.response(schemas.DetailedTrainerSchema())
    @ns.response(code=http_exceptions.Conflict.code)
    def patch(self, args, trainer):
        """
        Patch trainer details by ID.
        """
        self._abort_readonly(trainer.id)
        try:
            for operation in args:
                try:
                    if not self._process_patch_operation(operation, trainer=trainer):
                        log.info("Trainer patching has ignored unknown operation %s", operation)
                except ValueError as exception:
                    abort(code=http_exceptions.Conflict.code, message=str(exception))

            try:
                db.session.merge(trainer)
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                abort(
                    code=http_exceptions.Conflict.code,
                    message="Could not update trainer details."
                )
        finally:
            db.session.rollback()
        return trainer

    @ns.resolve_object_by_model(Trainer, 'trainer')
    @ns.response(code=http_exceptions.Conflict.code)
    def delete(self, trainer):
        """
        Delete a trainer by ID.
        """
        self._abort_readonly(trainer.id)
        teams = db.session.query(Team).filter(Team.trainer.has(Trainer.id == trainer.id))
        if teams.first() is not None:
            abort(
                code=http_exceptions.Forbidden.code,
                message="Cannot delete a trainer involved in a battle."
            )
        db.session.delete(trainer)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            # TODO: handle errors better
            abort(
                code=http_exceptions.Conflict.code,
                message="Could not delete the trainer."
            )
        return None

    def _process_patch_operation(self, operation, trainer):
        """
        Args:
            operation (dict) - one patch operation in RFC 6902 format.
            trainer (Trainer) - trainer instance which is needed to be patched.
            state (dict) - inter-operations state storage.

        Returns:
            processing_status (bool) - True if operation was handled, otherwise False.
        """
        if 'value' not in operation:
            # TODO: handle errors better
            abort(code=http_exceptions.UnprocessableEntity.code, message="value is required")

        assert operation['path'][0] == '/', "Path must always begin with /"
        field_name = operation['path'][1:]
        field_value = operation['value']

        if operation['op'] == parameters.PatchTrainerDetailsParameters.OP_REPLACE:
            setattr(trainer, field_name, field_value)
            return True

        return False

    def _abort_readonly(self, trainer_id):
        if trainer_id<=15:
            abort(
                code=http_exceptions.Forbidden.code,
                message="This trainer is read-only."
            )

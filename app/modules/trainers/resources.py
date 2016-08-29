# encoding: utf-8
"""
RESTful API Trainer resources
--------------------------
"""

import logging

from flask_restplus import Resource
import sqlalchemy

from app.extensions import db
from app.extensions.api import Namespace, abort, http_exceptions
from app.extensions.api.parameters import PaginationParameters
from app.modules.players.models import Player

from . import parameters, schemas
from .models import Trainer#, TeamMember


log = logging.getLogger(__name__) # pylint: disable=invalid-name
api = Namespace('trainers', description="Trainers") # pylint: disable=invalid-name


@api.route('/')
class Trainers(Resource):
    """
    Manipulations with trainers.
    """

    @api.parameters(PaginationParameters())
    @api.response(schemas.BaseTrainerSchema(many=True))
    def get(self, args):
        """
        List of trainers.

        Returns a list of trainers starting from ``offset`` limited by ``limit``
        parameter.
        """
        return Trainer.query.offset(args['offset']).limit(args['limit'])

    @api.parameters(parameters.CreateTrainerParameters())
    @api.response(schemas.DetailedTrainerSchema())
    @api.response(code=http_exceptions.Conflict.code)
    def post(self, args):
        """
        Create a new trainer.
        """
        try:
            try:
                trainer = Trainer(**args)
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


@api.route('/<int:trainer_id>')
@api.response(
    code=http_exceptions.NotFound.code,
    description="Trainer not found.",
)
class TrainerByID(Resource):
    """
    Manipulations with a specific trainer.
    """

    @api.resolve_object_by_model(Trainer, 'trainer')
    @api.response(schemas.DetailedTrainerSchema())
    def get(self, trainer):
        """
        Get trainer details by ID.
        """
        return trainer

    @api.resolve_object_by_model(Trainer, 'trainer')
    @api.parameters(parameters.PatchTrainerDetailsParameters())
    @api.response(schemas.DetailedTrainerSchema())
    @api.response(code=http_exceptions.Conflict.code)
    def patch(self, args, trainer):
        """
        Patch trainer details by ID.
        """
        try:
            for operation in args:
                try:
                    if not self._process_patch_operation(operation, trainer=trainer):
                        log.info("Trainer patching has ignored unknown operation %s", operation)
                except ValueError as exception:
                    abort(code=http_exceptions.Conflict.code, message=str(exception))

            db.session.merge(trainer)

            try:
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                abort(
                    code=http_exceptions.Conflict.code,
                    message="Could not update trainer details."
                )
        finally:
            db.session.rollback()
        return trainer

    @api.resolve_object_by_model(Trainer, 'trainer')
    @api.response(code=http_exceptions.Conflict.code)
    def delete(self, trainer):
        """
        Delete a trainer by ID.
        """
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


# @api.route('/<int:team_id>/members/')
# @api.response(
#     code=http_exceptions.NotFound.code,
#     description="Team not found.",
# )
# class TeamMembers(Resource):
#     """
#     Manipulations with members of a specific team.
#     """
#
#     @api.resolve_object_by_model(Team, 'team')
#     @api.parameters(PaginationParameters())
#     @api.response(schemas.BaseTeamMemberSchema(many=True))
#     def get(self, args, team):
#         """
#         Get team members by team ID.
#         """
#         return team.members[args['offset']: args['offset'] + args['limit']]
#
#     @api.resolve_object_by_model(Team, 'team')
#     @api.parameters(parameters.AddTeamMemberParameters())
#     @api.response(schemas.BaseTeamMemberSchema())
#     @api.response(code=http_exceptions.Conflict.code)
#     def post(self, args, team):
#         """
#         Add a new member to a team.
#         """
#         try:
#             player_id = args.pop('player_id')
#             player = Player.query.get(player_id)
#             if player is None:
#                 abort(
#                     code=http_exceptions.NotFound.code,
#                     message="Player with id %d does not exist" % player_id
#                 )
#
#             try:
#                 team_member = TeamMember(team=team, player=player, **args)
#             except ValueError as exception:
#                 abort(code=http_exceptions.Conflict.code, message=str(exception))
#
#             db.session.add(team_member)
#
#             try:
#                 db.session.commit()
#             except sqlalchemy.exc.IntegrityError:
#                 abort(
#                     code=http_exceptions.Conflict.code,
#                     message="Could not update team details."
#                 )
#         finally:
#             db.session.rollback()
#         return team_member
#
#
# @api.route('/<int:team_id>/members/<int:player_id>')
# @api.response(
#     code=http_exceptions.NotFound.code,
#     description="Team or member not found.",
# )
# class TeamMemberByID(Resource):
#     """
#     Manipulations with a specific team member.
#     """
#
#     @api.resolve_object_by_model(Team, 'team')
#     @api.response(code=http_exceptions.Conflict.code)
#     def delete(self, team, player_id):
#         """
#         Remove a member from a team.
#         """
#         team_member = TeamMember.query.filter_by(team=team, player_id=player_id).first_or_404()
#         db.session.delete(team_member)
#
#         try:
#             db.session.commit()
#         except sqlalchemy.exc.IntegrityError:
#             db.session.rollback()
#             # TODO: handle errors better
#             abort(
#                 code=http_exceptions.Conflict.code,
#                 message="Could not update team details."
#             )
#
#         return None

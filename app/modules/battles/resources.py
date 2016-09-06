# encoding: utf-8
# pylint: disable=too-few-public-methods,invalid-name
"""
RESTful API Battle resources
--------------------------
"""

import logging

from flask import Blueprint
from flask_login import current_user
from flask_restplus import Resource
#from flask_sockets import Sockets
import sqlalchemy
#from flask_socketio import emit

from app.extensions.api import Namespace, abort, http_exceptions, api_v1 as api
from app.extensions.api.parameters import PaginationParameters

from . import schemas, parameters, ns
from .models import db, Battle, Team, Location as CompositeLocation
from app.tasks import broadcast_battle
from app.modules.pokemons.models import Pokemon
from app.modules.pokemons.schemas import BasePokemonSchema
from app.modules.trainers.models import Trainer
from app.modules.trainers.schemas import DetailedTrainerSchema


log = logging.getLogger(__name__)


@ns.route('/')
class Battles(Resource):
    """
    Manipulations with battles.
    """

    @ns.parameters(parameters.BattleParameters())
    @ns.response(schemas.BaseBattleSchema(many=True))
    def get(self, args):
        """
        List of battles.

        Returns a list of battlees starting from ``offset`` limited by ``limit``
        parameter.
        """
        q = Battle.query
        print(args)
        if 'is_finished' in args:
            if args['is_finished']:
                q = q.filter(Battle.winner_id != None)
            else:
                q = q.filter(Battle.winner_id == None)
        return q.offset(args['offset']).limit(args['limit'])

    @ns.parameters(parameters.CreateBattleParameters(many=False), locations=('json',))
    #@ns.expect(parameters.CreateBattleParameters)
    @ns.response(schemas.BaseBattleSchema())
    @ns.response(code=http_exceptions.Conflict.code)
    def post(self, battle):
        """
        Create a new battle.
        """
        try:
            db.session.add(battle)
            try:
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                abort(code=http_exceptions.Conflict.code, message="Could not create a new battle.")
        finally:
            db.session.rollback()
        broadcast_battle.apply_async(args=[
                battle.id,
                schemas.BattleAPISchema().dump(battle).data
            ], eta=battle.start_time)
        print('delayed broadcast_battle')
        return battle


@ns.route('/<int:battle_id>')
@ns.response(
    code=http_exceptions.NotFound.code,
    description="Battle not found.",
)
class BattleByID(Resource):
    """
    Manipulations with a specific battle.
    """

    @ns.resolve_object_by_model(Battle, 'battle')
    @ns.response(schemas.DetailedBattleSchema())
    def get(self, battle):
        """
        Get battle details by ID.
        """
        #battle = Battle.query.options(db.joinedload('team1')).get_or_404(battle.id)
        return battle

    @ns.resolve_object_by_model(Battle, 'battle')
    @ns.response(code=http_exceptions.Conflict.code)
    def delete(self, battle):
        """
        Delete a battle by ID.
        """
        db.session.delete(battle)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            # TODO: handle errors better
            abort(
                code=http_exceptions.Conflict.code,
                message="Could not delete the battle."
            )
        return None


@ns.route('/<int:battle_id>/location')
class Location(Resource):
    @ns.resolve_object_by_model(Battle, 'battle')
    @ns.response(schemas.LocationSchema())
    def get(self, battle):
        """
        Get battle location.
        """
        return battle.location

    @ns.parameters(parameters.LocationParameters(), locations=('json',))
    #@ns.expect(parameters.LocationParameters, validate=True)
    @ns.resolve_object_by_model(Battle, 'battle')
    @ns.response(schemas.LocationSchema())
    def put(self, location_data, battle):
        """
        Set battle location.
        """
        try:
            try:
                battle.location = CompositeLocation(**location_data)
            except ValueError as exception:
                abort(code=http_exceptions.Conflict.code, message=str(exception))
            try:
                db.session.commit()
            except sqlalchemy.exc.IntegrityError as exception:
                abort(code=http_exceptions.Conflict.code, message="Could not set the location." + str(exception))
        finally:
            db.session.rollback()
        return battle.location


@ns.hide
@ns.route('/<int:battle_id>/outcome')
class Outcome(Resource):
    @ns.resolve_object_by_model(Battle, 'battle')
    #@ns.expect(parameters.outcome_parser, strict=True)
    @ns.parameters(parameters.OutcomeParameters())
    @ns.response(schemas.TeamSchema())
    #@ns.param('trainer_id', description='trainer ID of the winner')
    def put(self, args, battle):
        """
        Set a battle winner.
        """
        #args = parameters.outcome_parser.parse_args()
        winner = db.session.query(Team).filter(
            Team.trainer.has(Trainer.id == args['trainer_id']), Team.battle.contains(battle)
        ).first_or_404()

        battle.winner = winner
        db.session.commit()
        return winner


@ns.route('/<int:battle_id>/team<int:team_num>')
@ns.doc(responses={404: 'Battle not found'}, params={'team_num': '[1-2] (one of both teams)'})
class Teams(Resource):

    @staticmethod
    def get_battle_team(battle, team_num):
        try:
            return getattr(battle, "team%i" % team_num)
        except AttributeError:
            abort(404)

    @ns.resolve_object_by_model(Battle, 'battle')
    #@ns.doc(params={'team_num': '[1-2] (one of both teams)'})
    #@ns.parameters(parameters.TeamNumParameters())
    @ns.response(schemas.TeamSchema())
    def get(self, battle, team_num):
        """
        Get one of both teams
        """
        return self.get_battle_team(battle, team_num)


@ns.route('/<int:battle_id>/team<int:team_num>/trainer')
class TrainerByBattle(Resource):
    @ns.resolve_object_by_model(Battle, 'battle')
    @ns.response(DetailedTrainerSchema())
    def get(self, battle, team_num):
        """
        Get trainer from a team
        """
        return Teams.get_battle_team(battle, team_num).trainer


@ns.route('/<int:battle_id>/team<int:team_num>/pokemons/')
class Pokemons(Resource):
    @ns.resolve_object_by_model(Battle, 'battle')
    @ns.response(BasePokemonSchema(many=True))
    def get(self, battle, team_num):
        """
        List of pokemons from a team
        """
        return Teams.get_battle_team(battle, team_num).pokemons

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
from flask_sockets import Sockets
import sqlalchemy
#from flask_socketio import emit

from app.extensions.api import Namespace, abort, http_exceptions, api_v1 as api
from app.extensions.api.parameters import PaginationParameters

from . import schemas, parameters, ns
from .models import db, Battle, Team, Location
from app.tasks import broadcast_battle
from app.modules.pokemons.models import Pokemon
from app.modules.pokemons.schemas import BasePokemonSchema
from app.modules.trainers.schemas import DetailedTrainerSchema

import dateutil.parser

log = logging.getLogger(__name__)

ws = Blueprint(r'ws', __name__)

# @ws.route('/echo')
# def echo_socket(socket):
#     while not socket.closed:
#         message = socket.receive()
#         socket.send(message)

# @celery.task()
# def add_together(a, b):
#     print('add_together %i+%i' % (a, b))
#     return a + b
#
# @celery.task()
# def broadcast_battle(battle_id):
#     print('broadcasting battle...')
#     socketio.emit('message',
#                       {'data': 'Server generated event'},
#                       namespace='/battles')


@ns.route('/')
class Battles(Resource):
    """
    Manipulations with battles.
    """

    @ns.parameters(PaginationParameters())
    @ns.response(schemas.BaseBattleSchema(many=True))
    def get(self, args):
        """
        List of battles.

        Returns a list of battlees starting from ``offset`` limited by ``limit``
        parameter.
        """
        return Battle.query.offset(args['offset']).limit(args['limit'])

    @ns.expect(parameters.CreateBattleParameters)
    @ns.response(schemas.BaseBattleSchema())
    @ns.response(code=http_exceptions.Conflict.code)
    def post(self):
        """
        Create a new battle.
        """
        battle_data = api.payload
        try:
            try:
                battle, _ = schemas.CreateBattleSchema().load(battle_data)
                print(battle)
            except ValueError as exception:
                abort(code=http_exceptions.Conflict.code, message=str(exception))
            if battle.location is not None:
                db.session.add(battle.location)
            db.session.add(battle.team1)
            db.session.add(battle.team2)
            db.session.add(battle)
            try:
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                abort(code=http_exceptions.Conflict.code, message="Could not create a new battle.")
        finally:
            db.session.rollback()
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
        broadcast_battle.delay(
            battle.id,
            schemas.BattleAPISchema().dump(battle).data
        )
        print('delayed broadcast_battle')
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

        @ns.resolve_object_by_model(Battle, 'battle')
        @ns.expect(parameters.LocationParameters, validate=True)
        @ns.response(schemas.LocationSchema())
        def put(self, battle):
            """
            Set battle location.
            """
            try:
                try:
                    location =  if battle.location else Location(**api.payload)
                    battle.location = location
                except ValueError as exception:
                    abort(code=http_exceptions.Conflict.code, message=str(exception))
                db.session.add(location)
                db.session.add(battle)
                try:
                    db.session.commit()
                except sqlalchemy.exc.IntegrityError:
                    abort(code=http_exceptions.Conflict.code, message="Could not set the location.")
            finally:
                db.session.rollback()
            return location


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
class Trainer(Resource):
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





# @ns.route('/<int:battle_id>/points')
# class Points(Resource):
#     """
#     Manipulations with battlees' points.
#     """
#
#     @ns.resolve_object_by_model(Battle, 'battle')
#     @ns.parameters(parameters.AddPointParameters())
#     @ns.response(schemas.PointSchema())
#     @ns.response(code=http_exceptions.Conflict.code)
#     def post(self, args, battle):
#         """
#         Add a new point to a battle.
#         """
#         try:
#             player_id = args.pop('player_id')
#             player = Battle.query.get(battle_id)
#             if player is None:
#                 abort(
#                     code=http_exceptions.NotFound.code,
#                     message="Player with id %d does not exist" % player_id
#                 )
#             trainer_id = args.pop('trainer_id')
#             trainer = Battle.query.get(trainer_id)
#             if trainer is None:
#                 abort(
#                     code=http_exceptions.NotFound.code,
#                     message="Trainer with id %d does not exist" % trainer_id
#                 )
#
#             try:
#                 point = Point(battle=battle, trainer=trainer, player=player, **args)
#             except ValueError as exception:
#                 abort(code=http_exceptions.Conflict.code, message=str(exception))
#
#             db.session.add(point)
#
#             try:
#                 db.session.commit()
#             except sqlalchemy.exc.IntegrityError:
#                 abort(
#                     code=http_exceptions.Conflict.code,
#                     message="Could not update point details."
#                 )
#         finally:
#             db.session.rollback()
#         return point

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

from app.extensions.api import Namespace, abort, http_exceptions
from app.extensions.api.parameters import PaginationParameters

from . import schemas, parameters
from .models import db, Battle, Opponent, Location
from app.tasks import broadcast_battle
from app.modules.pokemons.models import Pokemon
from app.modules.pokemons.schemas import BasePokemonSchema
from app.modules.trainers.schemas import DetailedTrainerSchema

log = logging.getLogger(__name__)
api = Namespace('battles', description="Battles")
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

@api.route('/')
class Battles(Resource):
    """
    Manipulations with battles.
    """

    @api.parameters(PaginationParameters())
    @api.response(schemas.BaseBattleSchema(many=True))
    def get(self, args):
        """
        List of battles.

        Returns a list of battlees starting from ``offset`` limited by ``limit``
        parameter.
        """
        broadcast_battle.delay(1)
        print('delayed broadcast_battle')
        return Battle.query.offset(args['offset']).limit(args['limit'])

    @api.parameters(parameters.CreateBattleParameters())
    @api.response(schemas.BaseBattleSchema())
    @api.response(code=http_exceptions.Conflict.code)
    def post(self, args):
        """
        Create a new battle.
        """
        try:
            try:
                t1 = Opponent(trainer_id=args.pop("trainer1_id"))
                t2 = Opponent(trainer_id=args.pop("trainer2_id"))
                for pokemon_ids, team in [
                    (args.pop("opponent1_pokemons"), t1),
                    (args.pop("opponent2_pokemons"), t2)]:
                    for pokemon_id in pokemon_ids:
                        p = Pokemon.query.get(pokemon_id)
                        team.pokemons.append(p)
                battle = Battle(**args, opponent1=t1, opponent2=t2)
            except ValueError as exception:
                abort(code=http_exceptions.Conflict.code, message=str(exception))
            db.session.add(t1)
            db.session.add(t2)
            db.session.add(battle)
            try:
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                abort(code=http_exceptions.Conflict.code, message="Could not create a new battle.")
        finally:
            db.session.rollback()
        return battle


@api.route('/<int:battle_id>')
@api.response(
    code=http_exceptions.NotFound.code,
    description="Battle not found.",
)
class BattleByID(Resource):
    """
    Manipulations with a specific battle.
    """

    @api.resolve_object_by_model(Battle, 'battle')
    @api.response(schemas.DetailedBattleSchema())
    def get(self, battle):
        """
        Get battle details by ID.
        """
        return battle

    @api.resolve_object_by_model(Battle, 'battle')
    @api.response(code=http_exceptions.Conflict.code)
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

    @api.route('/<int:battle_id>/location')
    class Location(Resource):
        @api.resolve_object_by_model(Battle, 'battle')
        @api.response(schemas.LocationSchema())
        def get(self, battle):
            """
            Get battle location.
            """
            return battle.location

        @api.resolve_object_by_model(Battle, 'battle')
        @api.parameters(parameters.LocationParameters())
        @api.response(schemas.LocationSchema())
        def put(self, args, battle):
            """
            Set battle location.
            """
            try:
                try:
                    location = Location(**args)
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


@api.route('/<int:battle_id>/team<int:team_num>')
@api.doc(responses={404: 'Battle not found'}, params={'team_num': '[1-2] (one of both teams)'})
class Opponents(Resource):

    @staticmethod
    def get_battle_opponent(battle, team_num):
        try:
            return getattr(battle, "opponent%i" % team_num)
        except AttributeError:
            abort(404)

    @api.resolve_object_by_model(Battle, 'battle')
    #@api.doc(params={'team_num': '[1-2] (one of both teams)'})
    #@api.parameters(parameters.OpponentParameters())
    @api.response(schemas.OpponentSchema())
    def get(self, battle, team_num):
        """
        Get one of both teams
        """
        return self.get_battle_opponent(battle, team_num)

@api.route('/<int:battle_id>/team<int:team_num>/trainer')
class Trainer(Resource):
    @api.resolve_object_by_model(Battle, 'battle')
    @api.response(DetailedTrainerSchema())
    def get(self, battle, team_num):
        """
        Get trainer from a team
        """
        return Opponents.get_battle_opponent(battle, team_num).trainer

@api.route('/<int:battle_id>/team<int:team_num>/pokemons/')
class Pokemons(Resource):
    @api.resolve_object_by_model(Battle, 'battle')
    @api.response(BasePokemonSchema(many=True))
    def get(self, battle, team_num):
        """
        List of pokemons from a team
        """
        print(Opponents.get_battle_opponent(battle, team_num).pokemons)
        return Opponents.get_battle_opponent(battle, team_num).pokemons





# @api.route('/<int:battle_id>/points')
# class Points(Resource):
#     """
#     Manipulations with battlees' points.
#     """
#
#     @api.resolve_object_by_model(Battle, 'battle')
#     @api.parameters(parameters.AddPointParameters())
#     @api.response(schemas.PointSchema())
#     @api.response(code=http_exceptions.Conflict.code)
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

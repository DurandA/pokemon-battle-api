# encoding: utf-8
"""
Player database models
--------------------
"""
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import types as column_types, Timestamp

from app.extensions import db
from app.modules.trainers.models import Trainer
from app.modules.pokemons.models import Pokemon

import datetime


# pokemons = db.Table('battle_pokemons',
#     db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id')),
#     db.Column('battle_id', db.Integer, db.ForeignKey('battle.id'))
# )

class Location(db.Model):
    lat = db.Column(db.Float, primary_key=True)
    lng = db.Column(db.Float, primary_key=True)


# class OpponentPokemon(db.Model):
#     """
#     Opponent-pokemon database model.
#     """
#     __tablename__ = 'opponent_pokemon'
#
#     opponent_id = db.Column(db.Integer, db.ForeignKey('opponent.id'), primary_key=True)
#     opponent = db.relationship(
#         'Opponent',
#         backref=db.backref('pokemons')
#     )
#     pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), primary_key=True)
#     pokemon = db.relationship(
#         'Pokemon',
#         backref=db.backref('opponent_membership', cascade='delete, delete-orphan')
#     )

opponent_pokemon = db.Table('opponent_pokemon', db.Model.metadata,
    db.Column('opponent_id', db.Integer, db.ForeignKey('opponent.id')),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'))
)


class Opponent(db.Model):
    """
    Battle-member database model.
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # pylint: disable=invalid-name


    battle = db.relationship("Battle",
                primaryjoin="or_(Opponent.id==Battle.opponent1_id, "
                    "Opponent.id==Battle.opponent2_id)")
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'))
    trainer = db.relationship(
        'Trainer',
        backref=db.backref('battles_membership', cascade='delete, delete-orphan')
    )
    pokemons = db.relationship("Pokemon",
                    secondary=opponent_pokemon)


class Battle(db.Model, Timestamp):
    """
    Battle database model.
    """

    id = db.Column(db.Integer, primary_key=True) # pylint: disable=invalid-name

    opponent1_id = db.Column(db.Integer, db.ForeignKey('opponent.id'))
    opponent1 = db.relationship('Opponent', foreign_keys=[opponent1_id])
    opponent2_id = db.Column(db.Integer, db.ForeignKey('opponent.id'))
    opponent2 = db.relationship('Opponent', foreign_keys=[opponent2_id])
    lat = db.Column(db.Float, db.ForeignKey('location.lat'))
    lng = db.Column(db.Float, db.ForeignKey('location.lng'))
    location = db.relationship('Location', foreign_keys=[lat, lng], single_parent=True, cascade='delete')

    # pokemons = db.relationship('Pokemon', secondary=pokemons,
    #     backref=db.backref('battles', lazy='dynamic'))
    start_time = db.Column(db.DateTime, nullable=False)

    # @property
    # def is_finished(self):
    #     return datetime.datetime.now() > self.start_time + datetime.timedelta(minutes = 90)

    __table_args__ = (
        db.CheckConstraint('opponent1_id != opponent2_id', name='_opponent_cc'),
        db.ForeignKeyConstraint(
            ['lat', 'lng'],
            ['location.lat', 'location.lng'],
        ),
    )

    def __repr__(self):
        return (
            "<{class_name}("
            "id={self.id}, "
            "team1_id=\"{self.opponent1_id}\", "
            "team2_id=\"{self.opponent2_id}\", "
            "start_time=\"{self.start_time}\", "
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )


# class Point(db.Model):
#     """
#     Point database model.
#     """
#
#     match_id = db.Column(db.Integer, db.ForeignKey('match.id'), primary_key=True) # pylint: disable=invalid-name
#     match = db.relationship(
#         'Match',
#         backref=db.backref('points')
#     )
#     team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
#     team = db.relationship(
#         'Team',
#         backref=db.backref('points')
#     )
#     player_id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True)
#     player = db.relationship(
#         'Player',
#         backref=db.backref('points')
#     )
#     timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, primary_key=True)
#     value = db.Column(db.Integer, default=1, nullable=False)

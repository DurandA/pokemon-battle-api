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


class Location(object):
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def __composite_values__(self):
        return self.lat, self.lng

    def __repr__(self):
        return (
            "<{class_name}("
            "lat=\"{self.lat}\", "
            "lng=\"{self.lng}\""
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )

    def __eq__(self, other):
        return isinstance(other, Location) and \
            other.lat == self.lat and \
            other.lng == self.lng

    def __ne__(self, other):
        return not self.__eq__(other)


team_pokemon = db.Table('team_pokemon', db.Model.metadata,
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'))
)


class Team(db.Model):
    """
    Battle-member database model.
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # pylint: disable=invalid-name


    battle = db.relationship("Battle",
                primaryjoin="or_(Team.id==Battle.team1_id, "
                    "Team.id==Battle.team2_id)")
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'))
    trainer = db.relationship(
        'Trainer',
        backref=db.backref('battles_membership', cascade='delete, delete-orphan')
    )
    pokemons = db.relationship("Pokemon",
                    secondary=team_pokemon)


class Battle(db.Model, Timestamp):
    """
    Battle database model.
    """

    id = db.Column(db.Integer, primary_key=True) # pylint: disable=invalid-name

    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team1 = db.relationship('Team', foreign_keys=[team1_id])
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team2 = db.relationship('Team', foreign_keys=[team2_id])
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    location = db.composite(Location, lat, lng)
    winner_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    winner = db.relationship('Team', foreign_keys=[winner_id], single_parent=True)
    # pokemons = db.relationship('Pokemon', secondary=pokemons,
    #     backref=db.backref('battles', lazy='dynamic'))
    start_time = db.Column(db.DateTime, nullable=False)

    @property
    def end_time(self):
        return self.updated if self.winner else None

    __table_args__ = (
        db.CheckConstraint('team1_id != team2_id', name='_team_cc'),
    )

    __mapper_args__ = {
        "order_by": start_time
    }

    def __init__(self, *args, location=None, **kwargs):
        if location:
            self.location = Location(**location)
        super(Battle, self).__init__(*args, **kwargs)

    def __repr__(self):
        return (
            "<{class_name}("
            "id={self.id}, "
            "team1_id=\"{self.team1_id}\", "
            "team2_id=\"{self.team2_id}\", "
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

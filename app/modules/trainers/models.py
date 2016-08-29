# encoding: utf-8
"""
Team database models
--------------------
"""

from sqlalchemy_utils import Timestamp

from app.extensions import db


# class TeamMember(db.Model):
#     """
#     Team-member database model.
#     """
#     __tablename__ = 'team_member'
#
#     team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
#     team = db.relationship('Team')
#     player_id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True)
#     player = db.relationship(
#         'Player',
#         backref=db.backref('teams_membership', cascade='delete, delete-orphan')
#     )
#
#     is_leader = db.Column(db.Boolean, default=False, nullable=False)
#
#     __table_args__ = (
#         db.UniqueConstraint('team_id', 'player_id', name='_team_player_uc'),
#     )
#
#     def __repr__(self):
#         return (
#             "<{class_name}("
#             "team_id={self.team_id}, "
#             "player_id=\"{self.player_id}\", "
#             "is_leader=\"{self.is_leader}\""
#             ")>".format(
#                 class_name=self.__class__.__name__,
#                 self=self
#             )
#         )


class Trainer(db.Model, Timestamp):
    """
    Trainer database model.
    """

    id = db.Column(db.Integer, primary_key=True) # pylint: disable=invalid-name
    first_name = db.Column(db.String(length=30), default='', nullable=False)
    last_name = db.Column(db.String(length=30), default='', nullable=False)
    gender = db.Column(db.Enum("female", "male", name="gender_enum"), nullable=False)

    #members = db.relationship('TeamMember', cascade='delete, delete-orphan')
    #matches = db.relationship('Match')
    # battle_member = db.relationship('Opponent',
    #                 primaryjoin="or_(Trainer.id==Opponent.trainer1_id, "
    #                     "Trainer.id==Opponent.trainer2_id)")

    def __repr__(self):
        return (
            "<{class_name}("
            "id={self.id}, "
            "first_name=\"{self.first_name}\""
            "last_name=\"{self.last_name}\""
            "gender=\"{self.gender}\""
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )

    # @db.validates('title')
    # def validate_title(self, key, title): # pylint: disable=unused-argument,no-self-use
    #     if len(title) < 3:
    #         raise ValueError("Title has to be at least 3 characters long.")
    #     return title

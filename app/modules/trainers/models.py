# encoding: utf-8
"""
Team database models
--------------------
"""

from sqlalchemy_utils import Timestamp

from app.extensions import db


class Trainer(db.Model, Timestamp):
    """
    Trainer database model.
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # pylint: disable=invalid-name
    name = db.Column(db.String(length=30), default='', nullable=False)
    gender = db.Column(db.Enum("female", "male", name="gender_enum"), nullable=False)
    country_code =  db.Column(db.String(length=3), default='', nullable=False) # ISO 30166
    # battle_member = db.relationship('Opponent',
    #                 primaryjoin="or_(Trainer.id==Team.trainer1_id, "
    #                     "Trainer.id==Team.trainer2_id)")

    __table_args__ = (
        {'sqlite_autoincrement': True}
    )

    def __repr__(self):
        return (
            "<{class_name}("
            "id={self.id}, "
            "name=\"{self.name}\", "
            "gender=\"{self.gender}\", "
            "country=\"{self.country_code}\""
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )

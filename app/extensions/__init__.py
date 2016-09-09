# encoding: utf-8
# pylint: disable=invalid-name,wrong-import-position
"""
Extensions setup
================

Extensions provide access to common resources of the application.

Please, put new extension instantiations and initializations here.
"""

from flask_cors import CORS
cross_origin_resource_sharing = CORS()

from sqlalchemy_utils import force_auto_coercion, force_instant_defaults
force_auto_coercion()
force_instant_defaults()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_login import LoginManager
login_manager = LoginManager()

from flask_marshmallow import Marshmallow
marshmallow = Marshmallow()

from celery import Celery
celery = Celery(__name__, broker='redis://')

from flask_socketio import SocketIO
socketio = SocketIO()

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr
limiter = Limiter(key_func=get_ipaddr, storage_uri ="redis://", strategy="moving-window")

from . import api

from .auth import OAuth2Provider
oauth2 = OAuth2Provider()


class AlembicDatabaseMigrationConfig(object):
    """
    Helper config holder that provides missing functions of Flask-Alembic
    package since we use custom invoke tasks instead.
    """

    def __init__(self, database, directory='migrations', **kwargs):
        self.db = database
        self.directory = directory
        self.configure_args = kwargs


def init_app(app):
    """
    Application extensions initialization.
    """
    for extension in (
            cross_origin_resource_sharing,
            db,
            login_manager,
            marshmallow,
            api,
            oauth2,
            #socketio,
            limiter,
    ):
        extension.init_app(app)

    #celery.conf.update(CELERYBEAT_SCHEDULE = app.config['CELERYBEAT_SCHEDULE'])
    socketio.init_app(app, async_mode='eventlet', message_queue='redis://')
    app.extensions['migrate'] = AlembicDatabaseMigrationConfig(db, compare_type=True)

# encoding: utf-8
"""
Matches module
============
"""

from app.extensions.api import api_v1, Namespace
ns = Namespace('battles', description="Battles")
#from . import websockets
#from flask_sockets import Sockets


def init_app(app, **kwargs):
    # pylint: disable=unused-argument
    """
    Init battles module.
    """

    # Touch underlying modules
    from . import models, resources

    api_v1.add_namespace(ns)
    #sockets = Sockets(app)
    #sockets.register_blueprint(resources.ws)

# encoding: utf-8
"""
Matches module
============
"""

from app.extensions.api import api_v1
#from . import websockets
#from flask_sockets import Sockets


def init_app(app, **kwargs):
    # pylint: disable=unused-argument
    """
    Init battles module.
    """
    #socketio = app.extensions['socketio']

    # Touch underlying modules
    from . import models, resources
    #socketio = SocketIO(app, async_mode='eventlet', message_queue='redis://')
    #
    # @socketio.on('message', namespace='/test')
    # def echo(message):
    #     emit('message', message)
    #
    # socketio.on_event('echo', websockets.async_test, namespace='/test')
    print ('asdf')
    api_v1.add_namespace(resources.api)
    #sockets = Sockets(app)
    #sockets.register_blueprint(resources.ws)

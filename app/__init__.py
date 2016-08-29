# encoding: utf-8
"""
Example RESTful API Server.
"""
import logging
import os

import eventlet
from flask import Flask
from celery import Celery
from flask_socketio import SocketIO

# def make_celery(app):
#     celery = Celery(app.import_name, #backend=app.config['CELERY_BACKEND'],
#                     broker=app.config['CELERY_BROKER_URL'])
#     celery.conf.update(app.config)
#     app.extensions['celery'] = celery
#     TaskBase = celery.Task
#     class ContextTask(TaskBase):
#         abstract = True
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#     celery.Task = ContextTask
#     return celery

celery = Celery(__name__, broker='redis://')

CONFIG_NAME_MAPPER = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig',
    'local': 'local_config.LocalConfig',
}

def create_app(flask_config='production', **kwargs):
    """
    Entry point to the Flask RESTful Server application.
    """
    eventlet.monkey_patch()
    app = Flask(__name__, **kwargs)

    config_name = os.getenv('FLASK_CONFIG', flask_config)
    app.config.from_object(CONFIG_NAME_MAPPER[config_name])

    if app.debug:
        logging.getLogger('flask_oauthlib').setLevel(logging.DEBUG)
        app.logger.setLevel(logging.DEBUG)

        # We don't need default Flask's loggers when using invoke tasks as the
        # latter set up colorful loggers.
        for handler in app.logger.handlers:
            app.logger.removeHandler(handler)

    app.config.update(
        CELERY_BROKER_URL='redis://'#'sqla+sqlite:///celerydb.sqlite',
        #CELERY_RESULT_BACKEND='redis://localhost:6379'
    )
    celery.conf.update(app.config)
    #celery = make_celery(app)

    socketio = SocketIO(app, async_mode='eventlet', message_queue='redis://')

    from . import extensions
    extensions.init_app(app)

    from . import modules
    modules.init_app(app)#, celery_obj=celery)
    
    return app

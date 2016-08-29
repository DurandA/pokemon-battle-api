# encoding: utf-8
"""
API extension
=============
"""

from copy import deepcopy

from flask import Blueprint

from .api import Api
from .namespace import Namespace
from .http_exceptions import abort


api_v1 = Api( # pylint: disable=invalid-name
    version='1.0',
    title="Pokemon Battle API",
    description="Real-life example RESTful API server implementation using Flask-RESTplus",
)


def init_app(app, **kwargs):
    # pylint: disable=unused-argument
    """
    API extension initialization point.
    """
    if app.debug:
        @app.route('/swaggerui/<path:path>')
        def send_swaggerui_assets(path):
            # pylint: disable=unused-variable
            from flask import send_from_directory
            return send_from_directory('../static/', path)

    # Prevent config variable modification with runtime changes
    api_v1.authorizations = deepcopy(app.config['AUTHORIZATIONS'])

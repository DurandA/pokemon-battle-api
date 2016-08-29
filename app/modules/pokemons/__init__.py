# encoding: utf-8
"""
Pokemons module
============
"""

from app.extensions.api import api_v1


def init_app(app, **kwargs):
    # pylint: disable=unused-argument
    """
    Init pokemons module.
    """

    # Touch underlying modules
    with app.app_context():
        from . import models
    from . import resources

    api_v1.add_namespace(resources.api)

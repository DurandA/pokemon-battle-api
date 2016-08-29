# encoding: utf-8
"""
Sports module
============
"""

from app.extensions.api import api_v1


def init_app(app, **kwargs):
    # pylint: disable=unused-argument
    """
    Init pokemon types module.
    """

    # Touch underlying modules
    from . import resources

    api_v1.add_namespace(resources.api)

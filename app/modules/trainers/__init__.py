"""
Teams module
============
"""

from app.extensions.api import api_v1, Namespace
ns = Namespace('trainers', description="Trainers") # pylint: disable=invalid-name


def init_app(app, **kwargs):
    # pylint: disable=unused-argument
    """
    Init players module.
    """

    # Touch underlying modules
    from . import models, resources

    api_v1.add_namespace(ns)

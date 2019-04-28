# -*- coding: utf-8 -*-
"""
core package.
"""

__app__ = None


def _set_app(app):
    """
    sets the global instance of running application.
    this instance should not be accessed directly from packages outside of `bshop.core` package.
    outside packages, instead should access application functionality
    through `bshop.core.application.services` module.

    :param Application app: application instance.
    """

    global __app__
    __app__ = app


def _get_app():
    """
    gets the current instance of running application.

    :rtype: Application
    """

    global __app__
    return __app__

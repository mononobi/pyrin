# -*- coding: utf-8 -*-
"""
core package.
"""

__app__ = None


def _set_app(app):
    """
    sets the global instance of running application.
    this instance should not be accessed directly from packages outside of `bshop.core.application`
    package. but some internal `bshop.core` packages could use this instance if necessary for overcoming
    circular dependency problem. outside packages, instead should always access application
    functionality through `bshop.core.application.services` module.

    :param Application app: application instance.
    """

    global __app__
    __app__ = app


def _get_app():
    """
    gets the current instance of running application.
    this instance should not be accessed directly from packages outside of `bshop.core.application`
    package. but some internal `bshop.core` packages could use this instance if necessary for overcoming
    circular dependency problem. outside packages, instead should always access application
    functionality through `bshop.core.application.services` module.

    :rtype: Application
    """

    global __app__
    return __app__

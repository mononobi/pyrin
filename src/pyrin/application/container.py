# -*- coding: utf-8 -*-
"""
application container module.
"""

from threading import Lock

from pyrin.application.exceptions import ApplicationInstanceAlreadySetError


# holds the instance of running application.
__app__ = None
__lock__ = Lock()


def _set_app(app):
    """
    sets the global instance of running application.
    this instance should not be accessed directly from packages outside
    of `pyrin.application` package. but some internal `pyrin` packages could use
    this instance if necessary for overcoming circular dependency problem.
    outside packages, instead should always access application
    functionality through `pyrin.application.services` module.

    :raises ApplicationInstanceAlreadySetError: application instance already set error.

    :param Application app: application instance.
    """

    global __app__, __lock__

    try:
        __lock__.acquire()
        if __app__ is not None:
            raise ApplicationInstanceAlreadySetError('Application instance has been already '
                                                     'set, it could not be overwritten.')
        __app__ = app

    finally:
        if __lock__.locked():
            __lock__.release()


def _get_app():
    """
    gets the current instance of running application.
    this instance should not be accessed directly from packages outside
    of `pyrin.application` package. but some internal `pyrin` packages could use
    this instance if necessary for overcoming circular dependency problem.
    outside packages, instead should always access application
    functionality through `pyrin.application.services` module.

    :rtype: Application
    """

    global __app__
    return __app__

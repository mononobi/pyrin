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
    of `pyrin.application` package. outside packages, instead should always
    access application functionality through `pyrin.application.services` module.

    :param Application app: application instance.

    :raises ApplicationInstanceAlreadySetError: application instance already set error.
    """

    global __app__, __lock__

    message = 'Application instance has been already set, it could not be overwritten.'
    if __app__ is not None:
        raise ApplicationInstanceAlreadySetError(message)

    with __lock__:
        if __app__ is not None:
            raise ApplicationInstanceAlreadySetError(message)

        __app__ = app


def _get_app():
    """
    gets the current instance of running application.

    this instance should not be accessed directly from packages outside
    of `pyrin.application` package. outside packages, instead should always
    access application functionality through `pyrin.application.services` module.

    :rtype: Application
    """

    global __app__
    return __app__

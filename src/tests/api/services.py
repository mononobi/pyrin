# -*- coding: utf-8 -*-
"""
api services module.
"""

from werkzeug.exceptions import HTTPException

from pyrin.application.decorators import error_handler
from pyrin.application.services import get_component
from pyrin.core.exceptions import CoreException
from pyrin.api import APIPackage


@error_handler(HTTPException)
def handle_http_error(exception):
    """
    handles http exceptions.
    note that normally you should never call this method manually.

    :param HTTPException exception: exception instance.

    :rtype: CoreResponse
    """

    return get_component(APIPackage.COMPONENT_NAME).handle_http_error(exception)


@error_handler(CoreException)
def handle_server_error(exception):
    """
    handles server internal core exceptions.
    note that normally you should never call this method manually.

    :param CoreException exception: core exception instance.

    :rtype: CoreResponse
    """

    return get_component(APIPackage.COMPONENT_NAME).handle_server_error(exception)


@error_handler(Exception)
def handle_server_unknown_error(exception):
    """
    handles unknown server internal exceptions.
    note that normally you should never call this method manually.

    :param Exception exception: exception instance.

    :rtype: CoreResponse
    """

    return get_component(APIPackage.COMPONENT_NAME).handle_server_unknown_error(exception)

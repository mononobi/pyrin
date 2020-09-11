# -*- coding: utf-8 -*-
"""
api services module.
"""

from werkzeug.exceptions import HTTPException

from pyrin.application.decorators import error_handler
from pyrin.application.services import get_component
from pyrin.core.exceptions import CoreException, CoreBusinessException
from pyrin.api import APIPackage


@error_handler(HTTPException)
def handle_http_error(exception):
    """
    handles http exceptions.

    note that normally you should never call this method manually.

    :param HTTPException exception: exception instance.

    :returns: tuple[dict | object, int, CoreHeaders]
    :rtype: tuple
    """

    return get_component(APIPackage.COMPONENT_NAME).handle_http_error(exception)


@error_handler(CoreBusinessException)
def handle_server_business_error(exception):
    """
    handles server internal core business exceptions.

    note that normally you should never call this method manually.

    :param CoreBusinessException exception: core business exception instance.

    :returns: tuple[dict | object, int, CoreHeaders]
    :rtype: tuple
    """

    return get_component(APIPackage.COMPONENT_NAME).handle_server_business_error(exception)


@error_handler(CoreException)
def handle_server_error(exception):
    """
    handles server internal core exceptions.

    note that normally you should never call this method manually.
    in any environment which debug mode is False, the original error
    message will be replaced by a generic error message before being
    sent to client for security reasons.

    :param CoreException exception: core exception instance.

    :returns: tuple[dict | object, int, CoreHeaders]
    :rtype: tuple
    """

    return get_component(APIPackage.COMPONENT_NAME).handle_server_error(exception)


@error_handler(Exception)
def handle_server_unknown_error(exception):
    """
    handles unknown server internal exceptions.

    note that normally you should never call this method manually.
    in any environment which debug mode is False, the original error
    message will be replaced by a generic error message before being
    sent to client for security reasons.

    :param Exception exception: exception instance.

    :returns: tuple[dict | object, int, CoreHeaders]
    :rtype: tuple
    """

    return get_component(APIPackage.COMPONENT_NAME).handle_server_unknown_error(exception)


def register_hook(instance):
    """
    registers the given instance into api hooks.

    :param APIHookBase instance: api hook instance to be registered.

    :raises InvalidAPIHookTypeError: invalid api hook type error.
    """

    get_component(APIPackage.COMPONENT_NAME).register_hook(instance)

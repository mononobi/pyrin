# -*- coding: utf-8 -*-
"""
api error handlers module.
"""

from werkzeug.exceptions import HTTPException

import pyrin.logging.services as logging_services
import pyrin.security.session.services as session_services

from pyrin.application.decorators import error_handler
from pyrin.core.context import DTO
from pyrin.core.enumerations import ServerErrorResponseCodeEnum
from pyrin.core.exceptions import CoreException


@error_handler(HTTPException)
def http_error_handler(exception):
    """
    handler for http exceptions.

    :param HTTPException exception: exception instance.

    :returns: tuple(dict(int code: error code,
                         str message: error message),
                    int code: error code)

    :rtype: tuple(dict, int)
    """

    _log_error(exception)
    return DTO(code=exception.code,
               message=exception.description), exception.code


@error_handler(CoreException)
def server_error_handler(exception):
    """
    handler for server internal core exceptions.

    :param CoreException exception: core exception instance.

    :returns: tuple(dict(int code: error code,
                         str message: error message),
                    int code: error code)

    :rtype: tuple(dict, int)
    """

    _log_error(exception)
    return DTO(code=exception.code,
               message=exception.description), exception.code


@error_handler(Exception)
def server_unknown_error_handler(exception):
    """
    handler for unknown server internal exceptions.

    :param Exception exception: exception instance.

    :returns: tuple(dict(int code: error code,
                         str message: error message),
                    int code: error code)

    :rtype: tuple(dict, int)
    """

    _log_error(exception)
    return DTO(code=ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR,
               message=str(exception)), ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR


def _log_error(exception):
    """
    logs the specified exception.

    :param Exception exception: exception that caused on error.
    """

    client_request = session_services.get_current_request()
    logging_services.exception('{client_request} - {message}'
                               .format(client_request=client_request,
                                       message=str(exception)))

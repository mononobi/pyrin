# -*- coding: utf-8 -*-
"""
api error handlers module.
"""

from werkzeug.exceptions import HTTPException

from pyrin.application.decorators import error_handler
from pyrin.core.context import DTO
from pyrin.api.enumerations import ServerErrorResponseCodeEnum
from pyrin.core.exceptions import CoreException
from pyrin.utils.custom_print import print_error


@error_handler(HTTPException)
def http_error_handler(exception):
    """
    handler for http exceptions.

    :param HTTPException exception: exception instance.

    :returns: tuple(dict(int code: error code,
                         str message: error message), int code: error code)

    :rtype: tuple(dict, int)
    """
    print_error('ERROR-HTTP')
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
    print_error('ERROR-SERVER')
    return DTO(code=ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR,
               message=exception.description), ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR


@error_handler(Exception)
def server_unknown_error_handler(exception):
    """
    handler for unknown server internal exceptions.

    :param Exception exception: exception instance.

    :returns: tuple(dict(int code: error code,
                         str message: error message), int code: error code)

    :rtype: tuple(dict, int)
    """
    print_error('ERROR-UNKNOWN')
    return DTO(code=ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR,
               message=str(exception)), ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR

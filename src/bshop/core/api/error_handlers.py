# -*- coding: utf-8 -*-
"""
api error handlers module.
"""

from werkzeug.exceptions import HTTPException

from bshop.core.application.decorators import error_handler
from bshop.core.context import DTO
from bshop.core.api.enumerations import ServerErrorResponseCodeEnum
from bshop.core.exceptions import CoreException


@error_handler(HTTPException)
def http_error_handler(exception):
    """
    handler for http exceptions.

    :param HTTPException exception: exception instance.

    :returns: tuple(dict(int code: error code,
                         str message: error message), int code: error code)

    :rtype: tuple(dict, int)
    """
    print('ERROR-HTTP')
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
    print('ERROR-SERVER')
    return DTO(code=ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR.value,
               message=exception.message), ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR.value


@error_handler(Exception)
def server_unknown_error_handler(exception):
    """
    handler for unknown server internal exceptions.

    :param Exception exception: exception instance.

    :returns: tuple(dict(int code: error code,
                         str message: error message), int code: error code)

    :rtype: tuple(dict, int)
    """
    print('ERROR-UNKNOWN')
    return DTO(code=ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR.value,
               message=str(exception)), ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR.value

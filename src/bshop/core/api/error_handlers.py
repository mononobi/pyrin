# -*- coding: utf-8 -*-
"""
API error handlers module.
"""

from werkzeug.exceptions import HTTPException

from bshop.core import _get_app
from bshop.core.context import DTO
from bshop.core.api.enumeration import ServerErrorResponseCode
from bshop.core.exceptions import CoreException

app = _get_app()


@app.errorhandler(HTTPException)
def http_error_handler(exception):
    """
    Handler for http exceptions.

    :param HTTPException exception: exception instance.

    :returns: tuple(dict(int code: error code,
                         str message: error message), int code: error code)

    :rtype: tuple(dict, int)
    """
    print('ERROR-HTTP')
    return DTO(code=exception.code,
               message=exception.description), exception.code


@app.errorhandler(CoreException)
def server_error_handler(exception):
    """
    Handler for server internal core exceptions.

    :param CoreException exception: core exception instance.

    :returns: tuple(dict(int code: error code,
                         str message: error message),
                    int code: error code)

    :rtype: tuple(dict, int)
    """
    print('ERROR-SERVER')
    return DTO(code=ServerErrorResponseCode.INTERNAL_SERVER_ERROR.value,
               message=exception.message), ServerErrorResponseCode.INTERNAL_SERVER_ERROR.value


@app.errorhandler(Exception)
def server_unknown_error_handler(exception):
    """
    Handler for unknown server internal exceptions.

    :param Exception exception: exception instance.

    :returns: tuple(dict(int code: error code,
                         str message: error message), int code: error code)

    :rtype: tuple(dict, int)
    """
    print('ERROR-UNKNOWN')
    return DTO(code=ServerErrorResponseCode.INTERNAL_SERVER_ERROR.value,
               message=str(exception)), ServerErrorResponseCode.INTERNAL_SERVER_ERROR.value

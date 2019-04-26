# -*- coding: utf-8 -*-
"""
API error handlers module.
"""

from werkzeug.exceptions import HTTPException

from bshop.core.application import app
from bshop.core.context import DynamicObject
from bshop.core.api.enumeration import ServerErrorResponseCode
from bshop.core.exceptions import CoreException


@app.errorhandler(HTTPException)
def http_error_handler(exception):
    """
    Handler for http exceptions.

    :param HTTPException exception: exception instance.

    :returns: tuple(dict(int code: error code,
                         str message: error message), int code: error code)

    :rtype: tuple(dict, int)
    """

    return DynamicObject(code=exception.code,
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

    return DynamicObject(code=ServerErrorResponseCode.INTERNAL_SERVER_ERROR.value,
                         message=exception.message), \
        ServerErrorResponseCode.INTERNAL_SERVER_ERROR.value


@app.errorhandler(Exception)
def server_unknown_error_handler(exception):
    """
    Handler for unknown server internal exceptions.

    :param Exception exception: exception instance.

    :returns: tuple(dict(int code: error code,
                         str message: error message), int code: error code)

    :rtype: tuple(dict, int)
    """

    return DynamicObject(code=ServerErrorResponseCode.INTERNAL_SERVER_ERROR.value,
                         message=str(exception)), \
        ServerErrorResponseCode.INTERNAL_SERVER_ERROR.value

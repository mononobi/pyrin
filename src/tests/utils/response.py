# -*- coding: utf-8 -*-
"""
utils response module.
"""

from flask import make_response as flask_response

from pyrin.core.context import DTO
from pyrin.core.enumerations import ServerErrorResponseCodeEnum
from pyrin.settings.static import DEFAULT_STATUS_CODE


def make_response(message, **options):
    """
    makes a response from given inputs.

    :param str message: response message.

    :keyword int code: response code.
                       defaults to `DEFAULT_STATUS_CODE`, if not provided.

    :rtype: CoreResponse
    """

    code = options.get('code', DEFAULT_STATUS_CODE)
    response = DTO(code=code, message=message), code
    return flask_response(response)


def make_error_response(message, **options):
    """
    makes an error response from given inputs.

    :param str message: error message.

    :keyword int code: error code.
                       defaults to `INTERNAL_SERVER_ERROR` code, if not provided.

    :rtype: CoreResponse
    """

    code = options.get('code', ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR)
    return make_response(message, code=code)


def make_exception_response(exception, **options):
    """
    makes an error response from given exception.
    if the exception does not have code, defaults to `INTERNAL_SERVER_ERROR` code.

    :param Exception exception: exception instance.

    :keyword int code: error code.
                       tries to get it from exception itself, if not provided.
                       defaults to `INTERNAL_SERVER_ERROR` code.
                       if not available in exception.

    :rtype: CoreResponse
    """

    message = getattr(exception, 'description', str(exception))
    code = options.get('code', None)
    if code is None:
        code = getattr(exception, 'code', ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR)

    return make_error_response(message, code=code)

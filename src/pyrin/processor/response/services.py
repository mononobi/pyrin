# -*- coding: utf-8 -*-
"""
response services module.
"""

from pyrin.processor.response import ResponsePackage
from pyrin.application.services import get_component


def make_response(**options):
    """
    makes a response from given inputs.

    note that every other keyword argument that is present
    in given input, will be passed to generated response.

    :keyword int code: response code.
                       defaults to `DEFAULT_STATUS_CODE`
                       code, if not provided.

    :keyword dict headers: headers to add into response.

    :rtype: CoreResponse
    """

    return get_component(ResponsePackage.COMPONENT_NAME).make_response(**options)


def make_error_response(message, **options):
    """
    makes an error response from given inputs.

    :param str message: error message.

    :keyword int code: error code.
                       defaults to `INTERNAL_SERVER_ERROR`
                       code, if not provided.

    :keyword dict headers: headers to add into response.

    :rtype: CoreResponse
    """

    return get_component(ResponsePackage.COMPONENT_NAME).make_error_response(message,
                                                                             **options)


def make_exception_response(exception, **options):
    """
    makes an error response from given exception.

    if the exception does not have code, defaults
    to `INTERNAL_SERVER_ERROR` code.

    :param Exception exception: exception instance.

    :keyword int code: error code.
                       tries to get it from exception itself, if not
                       provided. defaults to `INTERNAL_SERVER_ERROR`
                       code if not available in exception.

    :keyword dict headers: headers to add into response.

    :rtype: CoreResponse
    """

    return get_component(ResponsePackage.COMPONENT_NAME).make_exception_response(exception,
                                                                                 **options)

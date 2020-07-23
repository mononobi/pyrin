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


def unpack_response(response, **options):
    """
    unpacks the response object into a tuple of three parts.

    in the form of `(body, status_code, headers)`. if any of these
    parts are not present in provided response, it returns None for
    that specific part.

    :param tuple | object response: response object to be unpacked.

    :returns: tuple[object body, int status_code, dict headers]
    :rtype: tuple[object, int, dict]
    """

    return get_component(ResponsePackage.COMPONENT_NAME).unpack_response(response,
                                                                         **options)


def pack_response(body, status_code, headers, **options):
    """
    packs the response using given values.

    it returns a tuple if status code or headers are
    not None, otherwise it just returns the body.

    :param object | CoreResponse body: body of response.
    :param int status_code: status code of response.
    :param dict headers: dict of response headers.

    :returns: tuple[object body, int status_code, dict headers] | object
    :rtype: tuple[object, int, dict] | object
    """

    return get_component(ResponsePackage.COMPONENT_NAME).pack_response(body, status_code,
                                                                       headers, **options)

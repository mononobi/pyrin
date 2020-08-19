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

    :keyword dict | Headers headers: headers to add into response.

    :returns: tuple[dict | object, int, CoreHeaders]
    :rtype: tuple
    """

    return get_component(ResponsePackage.COMPONENT_NAME).make_response(**options)


def make_error_response(message, **options):
    """
    makes an error response from given inputs.

    :param str message: error message.

    :keyword int code: error code.
                       defaults to `INTERNAL_SERVER_ERROR`
                       code, if not provided.

    :keyword dict | Headers headers: headers to add into response.

    :returns: tuple[dict | object, int, CoreHeaders]
    :rtype: tuple
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

    :keyword dict | Headers headers: headers to add into response.

    :returns: tuple[dict | object, int, CoreHeaders]
    :rtype: tuple
    """

    return get_component(ResponsePackage.COMPONENT_NAME).make_exception_response(exception,
                                                                                 **options)


def unpack_response(response, **options):
    """
    unpacks the response object into a tuple of three parts.

    in the form of `(body, status_code, headers)`. if any of these
    parts are not present in provided response, it returns None for
    that specific part.
    note that if a view function returns a `Response` object, the status
    code will be fetched from that object if available. but if a view function
    returns (Response response, int status_code) then the stand-alone status
    code will override the status code of `Response` object.

    :param tuple | object response: response object to be unpacked.

    :returns: tuple[object body, int status_code, CoreHeaders headers]
    :rtype: tuple[object, int, CoreHeaders]
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
    :param dict | Headers headers: all response headers.

    :returns: tuple[object body, int status_code, CoreHeaders headers] | object
    :rtype: tuple[object, int, CoreHeaders] | object
    """

    return get_component(ResponsePackage.COMPONENT_NAME).pack_response(body, status_code,
                                                                       headers, **options)


def get_body(response, **options):
    """
    gets the first part of a response tuple.

    it could be the body data or a response object itself.
    if response is not a tuple, the return value is the response itself.

    :param tuple | CoreResponse | object response: the response object
                                                   or instance or tuple.

    :rtype: CoreResponse | object
    """

    return get_component(ResponsePackage.COMPONENT_NAME).get_body(response, **options)

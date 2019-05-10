# -*- coding: utf-8 -*-
"""
application context module.
"""

from flask import Request, Response, jsonify

from pyrin.settings.application import APPLICATION_ENCODING
from pyrin.settings.api import JSONIFY_MIMETYPE, DEFAULT_STATUS_CODE


class CoreResponse(Response):
    """
    represents base response.
    this class should be used as server response.
    """

    # charset of the response.
    charset = APPLICATION_ENCODING

    # default status if none is provided.
    default_status = DEFAULT_STATUS_CODE

    # default mimetype if none is provided.
    default_mimetype = JSONIFY_MIMETYPE

    # function to use as response converter.
    response_converter = jsonify

    def __init__(self, response, **kwargs):
        super(CoreResponse, self).__init__(response, **kwargs)

    @classmethod
    def force_type(cls, response, environ=None):
        response = CoreResponse.response_converter(response)
        return super(CoreResponse, cls).force_type(response, environ)


class CoreRequest(Request):
    """
    represents base request class.
    this class should be used for server request.
    """

    # charset of the request.
    charset = APPLICATION_ENCODING

    def __init__(self, environ, populate_request=True, shallow=False):
        super(CoreRequest, self).__init__(environ, populate_request, shallow)

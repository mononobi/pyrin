# -*- coding: utf-8 -*-
"""
API context module.
"""

from flask import Request, Response, jsonify

from bshop.settings.application import APPLICATION_ENCODING
from bshop.settings.api import JSONIFY_MIMETYPE, DEFAULT_STATUS_CODE


class ResponseBase(Response):
    """
    Represents base response.
    This class should be used as server response.
    """

    # charset of the response.
    charset = APPLICATION_ENCODING

    # default status if none is provided.
    default_status = DEFAULT_STATUS_CODE

    # default mimetype if none is provided.
    default_mimetype = JSONIFY_MIMETYPE

    def __init__(self, response, **kwargs):
        super(ResponseBase, self).__init__(response, **kwargs)

    @classmethod
    def force_type(cls, response, environ=None):
        response = jsonify(response)
        return super(ResponseBase, cls).force_type(response, environ)


class RequestBase(Request):
    """
    Represents base request class.
    This class should be used for server request.
    """

    # charset of the request.
    charset = APPLICATION_ENCODING

    def __init__(self, environ, populate_request=True, shallow=False):
        super(RequestBase, self).__init__(environ, populate_request, shallow)

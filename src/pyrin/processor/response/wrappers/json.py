# -*- coding: utf-8 -*-
"""
response wrappers json module.
"""

from flask import jsonify

from pyrin.processor.mimetype.enumerations import MIMETypeEnum
from pyrin.processor.response.wrappers.base import CoreResponse


class JSONResponse(CoreResponse):
    """
    json response class.
    """

    default_mimetype = MIMETypeEnum.JSON

    # function to be used as response converter.
    response_converter = jsonify

    def __init__(self, response=None, status=None,
                 headers=None, direct_passthrough=False,
                 **options):
        """
        initializes an instance of JSONResponse.

        :param str | dict response: a json string or a dict object. if it
                                    is a dict, it will be converted to json.

        :param str | int status: a string with a status or an integer
                                 with the status code.

        :param list | Headers headers: a list of headers or a
                                       `datastructures.Headers` object.

        :param bool direct_passthrough: if set to True the `iter_encoded` method is not
                                        called before iteration which makes it
                                        possible to pass special iterators through
                                        unchanged.
        """

        if isinstance(response, dict):
            response = self.response_converter(response)

        super().__init__(response, status, headers,
                         mimetype=self.default_mimetype,
                         direct_passthrough=direct_passthrough,
                         **options)

    @classmethod
    def force_type(cls, response, environ=None):
        """
        enforce that the wsgi response is a response object of the current type.

        :param str | dict response: a json string or a dict object. if it
                                    is a dict, it will be converted to json.

        :param environ: a wsgi environment object.

        :rtype: CoreResponse
        """

        if isinstance(response, dict):
            response = cls.response_converter(response)

        return super().force_type(response, environ)

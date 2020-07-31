# -*- coding: utf-8 -*-
"""
response wrappers octet module.
"""

from pyrin.processor.mimetype.enumerations import MIMETypeEnum
from pyrin.processor.response.wrappers.base import CoreResponse


class OCTETResponse(CoreResponse):
    """
    octet response class.
    """

    default_mimetype = MIMETypeEnum.OCTET_STREAM

    def __init__(self, response=None, status=None,
                 headers=None, direct_passthrough=False,
                 **options):
        """
        initializes an instance of OCTETResponse.

        :param object response: an object containing the response value.

        :param str | int status: a string with a status or an integer
                                 with the status code.

        :param list | Headers headers: a list of headers or a
                                       `datastructures.Headers` object.

        :param bool direct_passthrough: if set to True the `iter_encoded` method is not
                                        called before iteration which makes it
                                        possible to pass special iterators through
                                        unchanged.

        :keyword dict original_data: a dict containing the original
                                     data of response before encoding.
                                     this value will be used in logging
                                     to mask critical values.
        """

        super().__init__(response, status, headers,
                         mimetype=self.default_mimetype,
                         direct_passthrough=direct_passthrough,
                         **options)

# -*- coding: utf-8 -*-
"""
utils headers module.
"""

from pyrin.core.structs import CoreHeaders


def convert_headers(headers, ignore_null=True):
    """
    converts given headers into a `CoreHeaders` objects.

    :param dict | Headers headers: headers to be converted.

    :param bool ignore_null: specifies that it must return a None
                             value if given headers input is None.
                             otherwise it returns an empty `CoreHeaders`.
                             defaults to True if not provided.


    :rtype: CoreHeaders
    """

    if headers is None and ignore_null is True:
        return headers
    elif headers is None:
        return CoreHeaders()

    return CoreHeaders(headers)

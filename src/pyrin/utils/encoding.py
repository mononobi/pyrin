# -*- coding: utf-8 -*-
"""
utils encoding module.
"""

import base64

from pyrin.settings.static import APPLICATION_ENCODING


def bytes_to_base64(value):
    """
    encodes the given raw bytes into base64 encoded bytes.

    :param bytes value: raw bytes value to be encoded into base64 bytes.

    :returns: base64 encoded bytes.

    :rtype: bytes
    """

    return base64.b64encode(value)


def base64_to_bytes(value):
    """
    decodes the given base64 encoded bytes value into raw bytes.

    :param bytes value: base64 encoded bytes value to be decoded into raw bytes.

    :returns: raw bytes.

    :rtype: bytes
    """

    return base64.b64decode(value)


def bytes_to_base64_string(value):
    """
    encodes the given raw bytes into base64 encoded bytes string.

    :param bytes value: raw bytes value to be encoded into base64 bytes string.

    :returns: base64 encoded bytes string.

    :rtype: str
    """

    return bytes_to_base64(value).decode(APPLICATION_ENCODING)


def base64_string_to_bytes(value):
    """
    decodes the given base64 encoded bytes string value into raw bytes.

    :param str value: base64 encoded bytes string value to be decoded into raw bytes.

    :returns: raw bytes.

    :rtype: bytes
    """

    return base64_to_bytes(value.encode(APPLICATION_ENCODING))

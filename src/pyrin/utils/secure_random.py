# -*- coding: utf-8 -*-
"""
utils secure random module.
"""

import secrets

from pyrin.settings.static import DEFAULT_SECURE_RANDOM_SIZE


def get_bytes(**options):
    """
    gets a secure random bytes with given length.
    the result value should not be decoded to string, because
    it's not a safe-string and may cause an error.
    if you want string representation, use `get_hex` or `get_url_safe` methods.

    :keyword int length: length of random bytes to be get.
                         if not provided, `DEFAULT_SECURE_RANDOM_SIZE` will be used.

    :rtype: bytes
    """

    length = options.get('length', DEFAULT_SECURE_RANDOM_SIZE)
    return secrets.token_bytes(length)


def get_hex(**options):
    """
    gets a secure random hex string with given length.

    :keyword int length: length of random string to be get in bytes.
                         if not provided, `DEFAULT_SECURE_RANDOM_SIZE` will be used.

    :rtype: str
    """

    length = options.get('length', DEFAULT_SECURE_RANDOM_SIZE)
    return secrets.token_hex(length)


def get_url_safe(**options):
    """
    gets a secure random url-safe string with given length.

    :keyword int length: length of random string to be get in bytes.
                         if not provided, `DEFAULT_SECURE_RANDOM_SIZE` will be used.

    :rtype: str
    """

    length = options.get('length', DEFAULT_SECURE_RANDOM_SIZE)
    return secrets.token_urlsafe(length)

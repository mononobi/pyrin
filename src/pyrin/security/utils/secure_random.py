# -*- coding: utf-8 -*-
"""
security utils secure_random module.
"""

import secrets

import pyrin.configuration.services as config_services


def get_bytes(**options):
    """
    gets a secure random bytes with given length.
    the result value should not be decoded to string, because
    it's not a safe-string and may cause an error.
    if you want string representation, use `get_hex` or `get_url_safe` methods.

    :keyword int length: length of random bytes to be get.
                         if not provided, `default_secure_random_size` config will be used.

    :rtype: bytes
    """

    length = options.get('length', None)
    if length is None:
        length = config_services.get('security', 'general',
                                     'default_secure_random_size')

    return secrets.token_bytes(length)


def get_hex(**options):
    """
    gets a secure random hex string with given length.

    :keyword int length: length of random string to be get in bytes.
                         if not provided, `default_secure_random_size` config will be used.

    :rtype: str
    """

    length = options.get('length', None)
    if length is None:
        length = config_services.get('security', 'general',
                                     'default_secure_random_size')

    return secrets.token_hex(length)


def get_url_safe(**options):
    """
    gets a secure random url-safe string with given length.

    :keyword int length: length of random string to be get in bytes.
                         if not provided, `default_secure_random_size` config will be used.

    :rtype: str
    """

    length = options.get('length', None)
    if length is None:
        length = config_services.get('security', 'general',
                                     'default_secure_random_size')

    return secrets.token_urlsafe(length)

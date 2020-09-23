# -*- coding: utf-8 -*-
"""
security utils services module.
"""

from pyrin.application.services import get_component
from pyrin.security.utils import SecurityUtilsPackage


def generate_rsa_key(length=None, **options):
    """
    generates a pair of public/private rsa keys.

    :param int length: key length in bits.
                       if not provided, `rsa_default_key_length`
                       config will be used.

    :returns: tuple[str public_key, str private_key]
    :rtype: tuple[str, str]
    """

    return get_component(SecurityUtilsPackage.COMPONENT_NAME).generate_rsa_key(length,
                                                                               **options)


def load_rsa_key(public_pem, private_pem, **options):
    """
    loads public/private rsa key objects from provided value.

    :param str public_pem: public key content to load from.
    :param str private_pem: private key content to load from.

    :returns: tuple[object public_key, object private_key]
    :rtype: tuple[object, object]
    """

    return get_component(SecurityUtilsPackage.COMPONENT_NAME).load_rsa_key(public_pem,
                                                                           private_pem,
                                                                           **options)


def get_bytes(length=None, **options):
    """
    gets a secure random bytes with given length.

    the result value should not be decoded to string, because
    it's not a safe-string and may cause an error.
    if you want string representation, use `get_hex` or `get_url_safe` methods.

    :param int length: length of random bytes to be get.
                       if not provided, `default_secure_random_size`
                       config will be used.

    :rtype: bytes
    """

    return get_component(SecurityUtilsPackage.COMPONENT_NAME).get_bytes(length, **options)


def get_hex(length=None, **options):
    """
    gets a secure random hex string with given length.

    :param int length: length of random string to be get in bytes.
                       if not provided, `default_secure_random_size`
                       config will be used.

    :rtype: str
    """

    return get_component(SecurityUtilsPackage.COMPONENT_NAME).get_hex(length, **options)


def get_url_safe(length=None, **options):
    """
    gets a secure random url-safe string with given length.

    :param int length: length of random string to be get in bytes.
                       if not provided, `default_secure_random_size`
                       config will be used.

    :rtype: str
    """

    return get_component(SecurityUtilsPackage.COMPONENT_NAME).get_url_safe(length, **options)

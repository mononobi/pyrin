# -*- coding: utf-8 -*-
"""
security utils key_helper module.
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

import pyrin.configuration.services as config_services

from pyrin.settings.static import APPLICATION_ENCODING


def generate_rsa_key(**options):
    """
    gets a pair of public/private rsa keys.

    :keyword int length: key length in bits.

    :returns: tuple(str public_key, str private_key)

    :rtype: tuple(str, str)
    """

    key_size = options.get('length', None)
    if key_size is None:
        key_size = config_services.get('security', 'general', 'rsa_default_key_length')

    key = rsa.generate_private_key(public_exponent=65537,
                                   key_size=key_size,
                                   backend=default_backend())

    private = key.private_bytes(encoding=serialization.Encoding.PEM,
                                format=serialization.PrivateFormat.TraditionalOpenSSL,
                                encryption_algorithm=serialization.NoEncryption())

    public_part = key.public_key()
    public = public_part.public_bytes(encoding=serialization.Encoding.PEM,
                                      format=serialization.PublicFormat.SubjectPublicKeyInfo)

    return public.decode(APPLICATION_ENCODING), private.decode(APPLICATION_ENCODING)


def load_rsa_key(public_pem, private_pem, **options):
    """
    loads public/private rsa key objects from provided value.

    :param str public_pem: public key content to load from.
    :param str private_pem: private key content to load from.

    :returns: tuple(public_key, private_key)

    :rtype: tuple(object, object)
    """

    private_key = serialization.load_pem_private_key(private_pem.encode(APPLICATION_ENCODING),
                                                     password=None,
                                                     backend=default_backend())

    public_key = serialization.load_pem_public_key(public_pem.encode(APPLICATION_ENCODING),
                                                   backend=default_backend())

    return public_key, private_key

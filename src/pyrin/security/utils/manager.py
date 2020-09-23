# -*- coding: utf-8 -*-
"""
security utils manager module.
"""

import secrets

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

import pyrin.configuration.services as config_services

from pyrin.core.structs import Manager
from pyrin.security.utils import SecurityUtilsPackage
from pyrin.settings.static import APPLICATION_ENCODING


class SecurityUtilsManager(Manager):
    """
    security utils manager class.
    """

    package_class = SecurityUtilsPackage

    def generate_rsa_key(self, length=None, **options):
        """
        generates a pair of public/private rsa keys.

        :param int length: key length in bits.
                           if not provided, `rsa_default_key_length`
                           config will be used.

        :returns: tuple[str public_key, str private_key]
        :rtype: tuple[str, str]
        """

        if length is None:
            length = config_services.get('security', 'general', 'rsa_default_key_length')

        key = rsa.generate_private_key(public_exponent=65537,
                                       key_size=length,
                                       backend=default_backend())

        private = key.private_bytes(encoding=serialization.Encoding.PEM,
                                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                                    encryption_algorithm=serialization.NoEncryption())

        public_part = key.public_key()
        public = public_part.public_bytes(encoding=serialization.Encoding.PEM,
                                          format=serialization.PublicFormat.SubjectPublicKeyInfo)

        return public.decode(APPLICATION_ENCODING), private.decode(APPLICATION_ENCODING)

    def load_rsa_key(self, public_pem, private_pem, **options):
        """
        loads public/private rsa key objects from provided value.

        :param str public_pem: public key content to load from.
        :param str private_pem: private key content to load from.

        :returns: tuple[object public_key, object private_key]
        :rtype: tuple[object, object]
        """

        private_key = serialization.load_pem_private_key(private_pem.encode(APPLICATION_ENCODING),
                                                         password=None,
                                                         backend=default_backend())

        public_key = serialization.load_pem_public_key(public_pem.encode(APPLICATION_ENCODING),
                                                       backend=default_backend())

        return public_key, private_key

    def get_bytes(self, length=None, **options):
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

        if length is None:
            length = config_services.get('security', 'general',
                                         'default_secure_random_size')

        return secrets.token_bytes(length)

    def get_hex(self, length=None, **options):
        """
        gets a secure random hex string with given length.

        :param int length: length of random string to be get in bytes.
                           if not provided, `default_secure_random_size`
                           config will be used.

        :rtype: str
        """

        if length is None:
            length = config_services.get('security', 'general',
                                         'default_secure_random_size')

        return secrets.token_hex(length)

    def get_url_safe(self, length=None, **options):
        """
        gets a secure random url-safe string with given length.

        :param int length: length of random string to be get in bytes.
                           if not provided, `default_secure_random_size`
                           config will be used.

        :rtype: str
        """

        if length is None:
            length = config_services.get('security', 'general',
                                         'default_secure_random_size')

        return secrets.token_urlsafe(length)

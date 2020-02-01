# -*- coding: utf-8 -*-
"""
aes128 encryption handler module.
"""

from cryptography.fernet import Fernet

import pyrin.configuration.services as config_services

from pyrin.security.encryption.decorators import encrypter
from pyrin.security.encryption.handlers.base import SymmetricEncrypterBase
from pyrin.settings.static import APPLICATION_ENCODING


@encrypter()
class AES128Encrypter(SymmetricEncrypterBase):
    """
    aes128 encrypter class.
    """

    def __init__(self, **options):
        """
        initializes an instance of AES128Encrypter.
        """

        super().__init__(**options)

        self._encrypter = Fernet(self._get_encryption_key(**options))

    def _get_encryption_key(self, **options):
        """
        gets the signing key for encryption.

        :rtype: str
        """

        return config_services.get('security', 'encryption', 'aes128_key')

    def _get_algorithm(self, **options):
        """
        gets the algorithm used for encryption.

        :rtype: str
        """

        return 'AES128'

    def _encrypt(self, text, **options):
        """
        encrypts the given value and returns the encrypted result.

        :param str text: text to be encrypted.

        :rtype: bytes
        """

        return self._encrypter.encrypt(text.encode(APPLICATION_ENCODING))

    def _decrypt(self, value, **options):
        """
        decrypts the given value and returns the decrypted result.

        :param bytes value: value to be decrypted.

        :rtype: str
        """

        return self._encrypter.decrypt(value).decode(APPLICATION_ENCODING)

    @classmethod
    def generate_key(cls, **options):
        """
        generates a valid key for this handler and returns it.

        :rtype: str
        """

        return Fernet.generate_key().decode(APPLICATION_ENCODING)

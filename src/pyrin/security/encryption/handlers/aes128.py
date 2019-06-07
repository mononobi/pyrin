# -*- coding: utf-8 -*-
"""
aes128 encryption handler module.
"""

from cryptography.fernet import Fernet

import pyrin.configuration.services as config_services

from pyrin.security.encryption.handlers.base import SymmetricEncrypterBase
from pyrin.settings.static import APPLICATION_ENCODING


class AES128Encrypter(SymmetricEncrypterBase):
    """
    aes encrypter class.
    """

    def __init__(self, **options):
        """
        initializes an instance of AESEncrypter.
        """

        # we pass the algorithm of encryption handler as the name of it.
        SymmetricEncrypterBase.__init__(self, self._get_algorithm(), **options)

        self._encrypter = Fernet(self._get_encryption_key(**options))

    def _get_encryption_key(self, **options):
        """
        gets the signing key for encryption.

        :rtype: str
        """

        return config_services.get('security', 'encryption', 'aes128_key')

    def _get_algorithm(self):
        """
        gets the algorithm used for encryption.

        :rtype: str
        """

        return 'AES128'

    def encrypt(self, value):
        """
        encrypts the given value and returns the encrypted result.

        :param str value: value to be encrypted.

        :rtype: str
        """

        return self._encrypter.encrypt(value).decode(APPLICATION_ENCODING)

    def decrypt(self, value):
        """
        decrypts the given value and returns the decrypted result.

        :param str value: value to be decrypted.

        :rtype: str
        """

        return self._encrypter.decrypt(value.encode(APPLICATION_ENCODING))

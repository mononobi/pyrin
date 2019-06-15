# -*- coding: utf-8 -*-
"""
security manager module.
"""

import pyrin.security.encryption.services as encryption_services
import pyrin.security.hashing.services as hashing_services

from pyrin.core.context import CoreObject
from pyrin.security.exceptions import InvalidPasswordLengthError, InvalidEncryptionTextLengthError


class SecurityManager(CoreObject):
    """
    security manager class.
    this class is intended to provide some services needed in pyrin application.
    the top level application must extend this class considering business requirements.
    """

    def get_password_hash(self, password, **options):
        """
        gets the given password's hash.

        :param str password: password to get it's hash.

        :keyword bool is_encrypted: specifies that given password is encrypted.

        :raises InvalidPasswordLengthError: invalid password length error.

        :rtype: str
        """

        if password is None or len(password) == 0:
            raise InvalidPasswordLengthError('Input password has invalid invalid.')

        decrypted_password = password
        is_encrypted = options.get('is_encrypted', False)
        if is_encrypted is True:
            decrypted_password = encryption_services.decrypt(password)

        hashed_password = hashing_services.generate_hash(decrypted_password)
        return hashed_password

    def encrypt(self, text, **options):
        """
        encrypts the given text and returns the encrypted value.

        :param str text: text to be encrypted.

        :raises InvalidEncryptionTextLengthError: invalid encryption text length error.

        :rtype: str
        """

        if text is None or len(text) == 0:
            raise InvalidEncryptionTextLengthError('Input text has invalid length.')

        return encryption_services.encrypt(text)

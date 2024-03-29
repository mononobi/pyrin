# -*- coding: utf-8 -*-
"""
security manager module.
"""

import pyrin.security.encryption.services as encryption_services
import pyrin.security.hashing.services as hashing_services

from pyrin.core.globals import _
from pyrin.core.structs import Manager
from pyrin.security import SecurityPackage
from pyrin.security.exceptions import InvalidPasswordLengthError, \
    InvalidEncryptionTextLengthError


class SecurityManager(Manager):
    """
    security manager class.
    """

    package_class = SecurityPackage

    def get_password_hash(self, password, **options):
        """
        gets the given password's hash.

        :param str password: password to get it's hash.

        :keyword bool is_encrypted: specifies that given password is encrypted.
                                    defaults to False if not provided.

        :raises InvalidPasswordLengthError: invalid password length error.

        :rtype: str
        """

        if password is None or len(password) == 0:
            raise InvalidPasswordLengthError(_('Input password has invalid length.'))

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
            raise InvalidEncryptionTextLengthError(_('Input text has invalid length.'))

        return encryption_services.encrypt(text)

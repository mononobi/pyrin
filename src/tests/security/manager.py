# -*- coding: utf-8 -*-
"""
security manager module.
"""

import pyrin.security.encryption.services as encryption_services
import pyrin.security.hashing.services as hashing_services

from pyrin.core.globals import _
from pyrin.core.context import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.security.exceptions import InvalidPasswordLengthError, InvalidUserError, \
    InvalidEncryptionTextLengthError


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

    def get_permission_ids(self, **options):
        """
        gets permission ids according to given inputs.

        :keyword dict user: user identity to get it's permission ids.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: list[permission_ids]

        :rtype: list[object]
        """

        raise CoreNotImplementedError()

    def get_user_permission_ids(self, user, **options):
        """
        gets specified user's permission ids.

        :param dict user: user identity to get it's permission ids.

        :raises InvalidUserError: invalid user error.

        :returns: list[permission_ids]

        :rtype: list[object]
        """

        if user is None:
            raise InvalidUserError(_('Input user could not be None.'))

        return self.get_permission_ids(user=user)

    def is_active(self, user, **options):
        """
        gets a value indicating that given user is active.

        :param dict user: user to check is active.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

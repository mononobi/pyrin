# -*- coding: utf-8 -*-
"""
security test_services module.
"""

from pyrin.application.services import get_component
from pyrin.security import SecurityPackage


def test_get_password_hash():
    """
    gets the given password's hash.

    :param str password: password to get it's hash.

    :keyword bool is_encrypted: specifies that given password is encrypted.

    :raises InvalidPasswordLengthError: invalid password length error.

    :rtype: str
    """



def test_encrypt():
    """
    encrypts the given text and returns the encrypted value.

    :param str text: text to be encrypted.

    :raises InvalidEncryptionTextLengthError: invalid encryption text length error.

    :rtype: str
    """



def test_get_permission_ids():
    """
    gets permission ids according to given inputs.

    :keyword dict user: user identity to get it's permission ids.

    :returns: list[permission_ids]

    :rtype: list[object]
    """



def get_user_permission_ids(user, **options):
    """
    gets specified user's permission ids.

    :param dict user: user identity to get it's permission ids.

    :raises InvalidUserError: invalid user error.

    :returns: list[permission_ids]

    :rtype: list[object]
    """


def is_active(user, **options):
    """
    gets a value indicating that given user is active.

    :param dict user: user to check is active.

    :rtype: bool
    """

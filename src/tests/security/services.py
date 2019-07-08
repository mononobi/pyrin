# -*- coding: utf-8 -*-
"""
security services module.
"""

from pyrin.application.services import get_component
from pyrin.security import SecurityPackage


def get_password_hash(password, **options):
    """
    gets the given password's hash.

    :param str password: password to get it's hash.

    :keyword bool is_encrypted: specifies that given password is encrypted.

    :raises InvalidPasswordLengthError: invalid password length error.

    :rtype: str
    """

    return get_component(SecurityPackage.COMPONENT_NAME).get_password_hash(password, **options)


def encrypt(text, **options):
    """
    encrypts the given text and returns the encrypted value.

    :param str text: text to be encrypted.

    :raises InvalidEncryptionTextLengthError: invalid encryption text length error.

    :rtype: str
    """

    return get_component(SecurityPackage.COMPONENT_NAME).encrypt(text, **options)


def get_permission_ids(**options):
    """
    gets permission ids according to given inputs.

    :keyword dict user: user identity to get it's permission ids.

    :returns: list[permission_ids]

    :rtype: list[object]
    """

    return get_component(SecurityPackage.COMPONENT_NAME).get_permission_ids(**options)


def get_user_permission_ids(user, **options):
    """
    gets specified user's permission ids.

    :param dict user: user identity to get it's permission ids.

    :raises InvalidUserError: invalid user error.

    :returns: list[permission_ids]

    :rtype: list[object]
    """

    return get_component(SecurityPackage.COMPONENT_NAME).get_user_permission_ids(user, **options)


def is_active(user, **options):
    """
    gets a value indicating that given user is active.

    :param dict user: user to check is active.

    :rtype: bool
    """

    return get_component(SecurityPackage.COMPONENT_NAME).is_active(user, **options)

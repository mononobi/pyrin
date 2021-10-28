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
                                defaults to False if not provided.

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

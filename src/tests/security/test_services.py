# -*- coding: utf-8 -*-
"""
security test_services module.
"""

import pytest

import pyrin.security.services as security_services
import pyrin.configuration.services as config_services

from pyrin.security.encryption.exceptions import InvalidEncryptedValueError
from pyrin.security.exceptions import InvalidPasswordLengthError, InvalidEncryptionTextLengthError


def test_get_password_hash():
    """
    gets the given password's hash.
    """

    password_hash = security_services.get_password_hash('secure password.')
    assert password_hash is not None and len(password_hash) > 0
    assert config_services.get('security', 'hashing',
                               'default_hashing_handler') in password_hash


def test_get_password_hash_encrypted_password():
    """
    gets the given password's hash which is encrypted.
    """

    encrypted_password = security_services.encrypt('normal password.')
    password_hash = security_services.get_password_hash(encrypted_password, is_encrypted=True)
    assert password_hash is not None and len(password_hash) > 0
    assert config_services.get('security', 'hashing',
                               'default_hashing_handler') in password_hash


def test_get_password_hash_invalid_password():
    """
    gets the given password's hash which has invalid value.
    it should raise an error.
    """

    with pytest.raises(InvalidPasswordLengthError):
        security_services.get_password_hash('')


def test_get_password_hash_invalid_encrypted_password():
    """
    gets the given password's hash which has invalid encrypted value.
    it should raise an error.
    """

    with pytest.raises(InvalidEncryptedValueError):
        security_services.get_password_hash('not encrypted.', is_encrypted=True)


def test_encrypt():
    """
    encrypts the given text and returns the encrypted value.
    """

    encrypted_value = security_services.encrypt('a confidential text.')
    assert encrypted_value is not None and len(encrypted_value) > 0
    assert config_services.get('security', 'encryption',
                               'default_encryption_handler') in encrypted_value


def test_encrypt_invalid_text():
    """
    encrypts the given text which has invalid length.
    it should raise an error.
    """

    with pytest.raises(InvalidEncryptionTextLengthError):
        security_services.encrypt('')

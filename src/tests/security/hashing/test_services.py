# -*- coding: utf-8 -*-
"""
hashing test_services module.
"""

import pytest

import pyrin.security.hashing.services as hashing_services
import pyrin.configuration.services as config_services

from pyrin.security.hashing.handlers.bcrypt import BcryptHashing
from pyrin.security.hashing.handlers.exceptions import BcryptMaxSizeLimitError
from pyrin.security.hashing.exceptions import DuplicatedHashingHandlerError, \
    InvalidHashingHandlerTypeError


def test_register_hashing_handler_duplicate():
    """
    registers a an already available hashing handler.
    it should raise an error.
    """

    with pytest.raises(DuplicatedHashingHandlerError):
        hashing_services.register_hashing_handler(BcryptHashing())


def test_register_hashing_handler_duplicate_with_replace():
    """
    registers a an already available hashing handler with replace option.
    it should not raise an error.
    """

    hashing_services.register_hashing_handler(BcryptHashing(), replace=True)


def test_register_hashing_handler_invalid_type():
    """
    registers a hashing handler with invalid type.
    it should raise an error.
    """

    with pytest.raises(InvalidHashingHandlerTypeError):
        hashing_services.register_hashing_handler(object())


def test_generate_hash_default():
    """
    gets the hash of input text using default handler.
    """

    value = hashing_services.generate_hash('text')
    default_handler = config_services.get('security', 'hashing', 'default_hashing_handler')
    assert value is not None
    assert default_handler in value


def test_generate_hash_bcrypt():
    """
    gets the hash of input text using bcrypt handler.
    """

    value = hashing_services.generate_hash('text', handler_name='bcrypt')
    assert value is not None
    assert 'bcrypt' in value


def test_generate_hash_bcrypt_invalid_length():
    """
    gets the hash of input text which has invalid length using bcrypt handler.
    """

    with pytest.raises(BcryptMaxSizeLimitError):
        hashing_services.generate_hash('01234567890123456789012345678901234567890123456789012345',
                                       handler_name='bcrypt')


def test_generate_hash_pbkdf2():
    """
    gets the hash of input text using pbkdf2 handler.
    """

    value = hashing_services.generate_hash('text', handler_name='PBKDF2')
    assert value is not None
    assert 'PBKDF2' in value


def test_is_match_default():
    """
    gets a value indicating that given texts hashes using default handler are match.
    """

    value = hashing_services.generate_hash('text')
    is_match = hashing_services.is_match('text', value)
    assert is_match is True


def test_is_match_bcrypt():
    """
    gets a value indicating that given texts hashes using bcrypt handler are match.
    """

    value = hashing_services.generate_hash('text', handler_name='bcrypt')
    is_match = hashing_services.is_match('text', value)
    assert is_match is True


def test_is_match_pbkdf2():
    """
    gets a value indicating that given texts hashes using pbkdf2 handler are match.
    """

    value = hashing_services.generate_hash('text', handler_name='PBKDF2')
    is_match = hashing_services.is_match('text', value)
    assert is_match is True

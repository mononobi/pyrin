# -*- coding: utf-8 -*-
"""
encryption test_services module.
"""

import pytest

import pyrin.security.encryption.services as encryption_services
import pyrin.configuration.services as config_services

from pyrin.security.encryption.handlers.aes128 import AES128Encrypter
from pyrin.security.encryption.handlers.rsa256 import RSA256Encrypter
from pyrin.security.encryption.exceptions import DuplicatedEncryptionHandlerError, \
    InvalidEncryptionHandlerTypeError, EncryptionHandlerNotFoundError, DecryptionError


def test_register_encryption_handler_duplicate():
    """
    registers an already available encryption handler.
    it should raise an error.
    """

    with pytest.raises(DuplicatedEncryptionHandlerError):
        encryption_services.register_encryption_handler(AES128Encrypter())


def test_register_encryption_handler_invalid_type():
    """
    registers an encryption handler with an invalid type.
    it should raise an error.
    """

    with pytest.raises(InvalidEncryptionHandlerTypeError):
        encryption_services.register_encryption_handler(25)


def test_register_encryption_handler_duplicate_with_replace():
    """
    registers an already available encryption handler with replace option.
    it should not raise an error.
    """

    encryption_services.register_encryption_handler(RSA256Encrypter(), replace=True)


def test_encrypt_default():
    """
    encrypts the given value using default handler and returns the encrypted result.
    """

    message = 'confidential'
    encrypted_value = encryption_services.encrypt(message)
    assert encrypted_value is not None
    assert config_services.get('security', 'encryption',
                               'default_encryption_handler') in encrypted_value


def test_encrypt_aes128():
    """
    encrypts the given value using aes128 handler and returns the encrypted result.
    """

    message = 'confidential'
    encrypted_value = encryption_services.encrypt(message, handler_name='AES128')
    assert encrypted_value is not None
    assert 'AES128' in encrypted_value


def test_encrypt_rsa256():
    """
    encrypts the given value using rsa256 handler and returns the encrypted result.
    """

    message = 'confidential'
    encrypted_value = encryption_services.encrypt(message, handler_name='RSA256')
    assert encrypted_value is not None
    assert 'RSA256' in encrypted_value


def test_encrypt_invalid_handler():
    """
    encrypts the given value using an invalid handler.
    it should raise an error.
    """

    with pytest.raises(EncryptionHandlerNotFoundError):
        encryption_services.encrypt('confidential', handler_name='missing_handler')


def test_decrypt_default():
    """
    decrypts the given full encrypted value using default
    handler and returns the decrypted result.
    """

    message = 'confidential'
    encrypted_value = encryption_services.encrypt(message)
    original_value = encryption_services.decrypt(encrypted_value)
    assert original_value == message


def test_decrypt_aes128():
    """
    decrypts the given full encrypted value using aes128
    handler and returns the decrypted result.
    """

    message = 'confidential'
    encrypted_value = encryption_services.encrypt(message, handler_name='AES128')
    original_value = encryption_services.decrypt(encrypted_value)
    assert original_value == message


def test_decrypt_rsa256():
    """
    decrypts the given full encrypted value using rsa256
    handler and returns the decrypted result.
    """

    message = 'confidential'
    encrypted_value = encryption_services.encrypt(message, handler_name='RSA256')
    original_value = encryption_services.decrypt(encrypted_value)
    assert original_value == message


def test_decrypt_invalid_value():
    """
    decrypts the given invalid encrypted value using default handler.
    it should raise an error.
    """

    with pytest.raises(DecryptionError):
        message = 'confidential'
        encrypted_value = encryption_services.encrypt(message)
        encrypted_value = encrypted_value.replace('o', 'b')
        encryption_services.decrypt(encrypted_value)


def test_decrypt_invalid_handler():
    """
    decrypts the given encrypted value using an invalid handler.
    it should raise an error.
    """

    with pytest.raises(EncryptionHandlerNotFoundError):
        message = 'confidential'
        encrypted_value = encryption_services.encrypt(message)
        handler = config_services.get('security', 'encryption',
                                      'default_encryption_handler')
        encrypted_value = encrypted_value.replace(handler, 'missing handler')
        encryption_services.decrypt(encrypted_value)


def test_decrypt_mismatch_handler():
    """
    decrypts the given encrypted value using a handler that is not the original handler.
    it should raise an error.
    """

    with pytest.raises(DecryptionError):
        message = 'confidential'
        handler = 'AES128'
        mismatch_handler = 'RSA256'
        encrypted_value = encryption_services.encrypt(message, handler_name=handler)
        encrypted_value = encrypted_value.replace(handler, mismatch_handler)
        encryption_services.decrypt(encrypted_value)


def test_generate_key_aes128():
    """
    generates a valid key for aes128 handler and returns it.
    """

    key = encryption_services.generate_key('AES128')
    assert key is not None and len(key) > 0


def test_generate_key_rsa256():
    """
    generates a valid public/private key pair for rsa256 handler and returns it.
    """

    public, private = encryption_services.generate_key('RSA256')
    assert public is not None and private is not None
    assert len(public) > 0 and len(private) > 0


def test_generate_key_invalid_handler():
    """
    generates a key for an invalid handler.
    it should raise an error.
    """

    with pytest.raises(EncryptionHandlerNotFoundError):
        encryption_services.generate_key('missing handler')


def test_encrypter_is_singleton():
    """
    tests that different types of encrypters are singleton.
    """

    encrypter1 = AES128Encrypter()
    encrypter2 = AES128Encrypter()

    assert encrypter1 == encrypter2

    encrypter3 = RSA256Encrypter()
    encrypter4 = RSA256Encrypter()

    assert encrypter3 == encrypter4

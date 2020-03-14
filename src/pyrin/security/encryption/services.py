# -*- coding: utf-8 -*-
"""
encryption services module.
"""

from pyrin.application.services import get_component
from pyrin.security.encryption import EncryptionPackage


def register_encryption_handler(instance, **options):
    """
    registers a new encryption handler or replaces the existing one
    if `replace=True` is provided. otherwise, it raises an error
    on adding an instance which it's name is already available
    in registered handlers.

    :param AbstractEncrypterBase instance: encryption handler to be registered.
                                           it must be an instance of AbstractEncrypterBase.

    :keyword bool replace: specifies that if there is another registered
                           handler with the same name, replace it with
                           the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidEncryptionHandlerTypeError: invalid encryption handler type error.
    :raises InvalidEncryptionHandlerNameError: invalid encryption handler name error.
    :raises DuplicatedEncryptionHandlerError: duplicated encryption handler error.
    """

    return get_component(EncryptionPackage.COMPONENT_NAME).register_encryption_handler(instance,
                                                                                       **options)


def encrypt(text, **options):
    """
    encrypts the given value using specified handler and returns the encrypted result.

    :param str text: text to be encrypted.

    :keyword str handler_name: handler name to be used for encryption.
                               if not provided, default handler from
                               relevant configs will be used.

    :raises EncryptionHandlerNotFoundError: encryption handler not found error.

    :rtype: str
    """

    return get_component(EncryptionPackage.COMPONENT_NAME).encrypt(text, **options)


def decrypt(full_encrypted_value, **options):
    """
    decrypts the given full encrypted value using specified
    handler and returns the decrypted result.

    :param str full_encrypted_value: full encrypted value to be decrypted.

    :raises InvalidEncryptionValueError: invalid encryption value error.
    :raises EncryptionHandlerNotFoundError: encryption handler not found error.
    :raises DecryptionError: decryption error.

    :rtype: str
    """

    return get_component(EncryptionPackage.COMPONENT_NAME).decrypt(full_encrypted_value,
                                                                   **options)


def generate_key(handler_name, **options):
    """
    generates a valid key for the given handler and returns it.

    :param str handler_name: handler name to be used for key generation.

    :keyword int length: the length of generated key in bytes.
                         note that some encryption handlers may not accept custom
                         key length so this value would be ignored on those handlers.

    :raises EncryptionHandlerNotFoundError: encryption handler not found error.

    :rtype: str | tuple[str, str]
    """

    return get_component(EncryptionPackage.COMPONENT_NAME).generate_key(handler_name, **options)

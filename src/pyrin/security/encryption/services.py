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

    :param EncrypterBase instance: encryption handler to be registered.
                                   it must be an instance of EncrypterBase.

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


def encrypt(handler_name, value):
    """
    encrypts the given value using specified handler and returns the encrypted result.

    :param str handler_name: handler name to be used for encryption.
    :param str value: value to be encrypted.

    :rtype: str
    """

    return get_component(EncryptionPackage.COMPONENT_NAME).encrypt(handler_name, value)


def decrypt(handler_name, value):
    """
    decrypts the given value using specified handler and returns the decrypted result.

    :param str handler_name: handler name to be used for decryption.
    :param str value: value to be decrypted.

    :rtype: str
    """

    return get_component(EncryptionPackage.COMPONENT_NAME).decrypt(handler_name, value)


def generate_key(handler_name, **options):
    """
    generates a valid key for the given handler and returns it.

    :param str handler_name: handler name to be used for key generation.

    :keyword int length: the length of generated key in bytes.
                         note that some encryption handlers may not accept custom
                         key length so this value would be ignored on those handlers.

    :rtype: Union[str, tuple(str, str)]
    """

    return get_component(EncryptionPackage.COMPONENT_NAME).generate_key(handler_name,
                                                                        **options)

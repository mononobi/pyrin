# -*- coding: utf-8 -*-
"""
encryption manager module.
"""

import pyrin.configuration.services as config_services

from pyrin.core.context import CoreObject, Context
from pyrin.security.encryption.exceptions import InvalidEncryptionHandlerTypeError, \
    InvalidEncryptionHandlerNameError, DuplicatedEncryptionHandlerError, \
    EncryptionHandlerNotFoundError, InvalidEncryptedValueError
from pyrin.security.encryption.handlers.base import EncrypterBase
from pyrin.utils.custom_print import print_warning


class EncryptionManager(CoreObject):
    """
    encryption manager class.
    """

    def __init__(self):
        """
        initializes an instance of EncryptionManager.
        """

        CoreObject.__init__(self)

        self._encryption_handlers = Context()
        self._separator = '$'

    def register_encryption_handler(self, instance, **options):
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

        if not isinstance(instance, EncrypterBase):
            raise InvalidEncryptionHandlerTypeError('Input parameter [{instance}] is '
                                                    'not an instance of EncrypterBase.'
                                                    .format(instance=str(instance)))

        if instance.get_name() is None or len(instance.get_name().strip()) == 0:
            raise InvalidEncryptionHandlerNameError('Encryption handler [{instance}] '
                                                    'has invalid name.'
                                                    .format(instance=str(instance)))

        # checking whether is there any registered instance with the same name.
        if instance.get_name() in self._encryption_handlers.keys():
            replace = options.get('replace', False)

            if replace is not True:
                raise DuplicatedEncryptionHandlerError('There is another registered encryption '
                                                       'handler with name [{name}] but "replace" '
                                                       'option is not set, so handler '
                                                       '[{instance}] could not be registered.'
                                                       .format(name=instance.get_name(),
                                                               instance=str(instance)))

            old_instance = self._encryption_handlers[instance.get_name()]
            print_warning('Encryption handler [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=str(old_instance), new_instance=str(instance)))

        # registering new encryption handler.
        self._encryption_handlers[instance.get_name()] = instance

    def encrypt(self, text, **options):
        """
        encrypts the given value using specified handler and returns the encrypted result.

        :param str text: text to be encrypted.

        :keyword str handler_name: handler name to be used for encryption.
                                   if not provided, default handler from
                                   relevant configs will be used.

        :rtype: str
        """

        return self._get_encryption_handler(**options).encrypt(text, **options)

    def decrypt(self, full_encrypted_value, **options):
        """
        decrypts the given full encrypted value using specified
        handler and returns the decrypted result.

        :param str full_encrypted_value: full encrypted value to be decrypted.

        :rtype: str
        """

        handler_name = self._extract_handler_name(full_encrypted_value, **options)
        return self._get_encryption_handler(handler_name=handler_name).decrypt(
            full_encrypted_value, **options)

    def generate_key(self, handler_name, **options):
        """
        generates a valid key for the given handler and returns it.

        :param str handler_name: handler name to be used for key generation.

        :keyword int length: the length of generated key in bytes.
                             note that some encryption handlers may not accept custom
                             key length so this value would be ignored on those handlers.

        :rtype: Union[str, tuple(str, str)]
        """

        return self._get_encryption_handler(handler_name=handler_name).generate_key(**options)

    def _get_encryption_handler(self, **options):
        """
        gets the specified encryption handler.

        :keyword str handler_name: handler name to get.
                                   if not provided, default handler from
                                   relevant configs will be used.

        :raises EncryptionHandlerNotFoundError: encryption handler not found error.

        :rtype: EncrypterBase
        """

        handler_name = options.get('handler_name', self._get_default_handler_name())
        if handler_name not in self._encryption_handlers.keys():
            raise EncryptionHandlerNotFoundError('Encryption handler [{name}] not found.'
                                                 .format(name=handler_name))

        return self._encryption_handlers[handler_name]

    def _get_default_handler_name(self):
        """
        gets default encryption handler name from configs.

        :rtype: str
        """

        return config_services.get('security', 'encryption', 'default_encryption_handler')

    def _extract_handler_name(self, full_encrypted_value, **options):
        """
        extracts the handler name of given full encrypted value.

        :param str full_encrypted_value: full encrypted value to extract
                                         the handler name from.

        :raises InvalidEncryptionValueError: invalid encryption value error.

        :rtype: str
        """

        if full_encrypted_value.count(self._separator) < 2:
            raise InvalidEncryptedValueError('Input encrypted value has an incorrect format.')

        items = full_encrypted_value.split(self._separator, 2)
        return items[1]

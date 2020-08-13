# -*- coding: utf-8 -*-
"""
hashing manager module.
"""

import pyrin.configuration.services as config_services

from pyrin.core.structs import Context, Manager
from pyrin.security.hashing import HashingPackage
from pyrin.security.hashing.interface import AbstractHashingBase
from pyrin.utils.custom_print import print_warning
from pyrin.security.hashing.exceptions import InvalidHashingHandlerTypeError, \
    InvalidHashingHandlerNameError, DuplicatedHashingHandlerError, InvalidHashError, \
    HashingHandlerNotFoundError


class HashingManager(Manager):
    """
    hashing manager class.
    """

    package_class = HashingPackage

    def __init__(self):
        """
        initializes an instance of HashingManager.
        """

        super().__init__()

        self._hashing_handlers = Context()
        self._separator = '$'

    def register_hashing_handler(self, instance, **options):
        """
        registers a new hashing handler or replaces the existing one
        if `replace=True` is provided. otherwise, it raises an error
        on adding an instance which it's name is already available
        in registered handlers.

        :param AbstractHashingBase instance: hashing handler to be registered.
                                             it must be an instance of AbstractHashingBase.

        :keyword bool replace: specifies that if there is another registered
                               handler with the same name, replace it with
                               the new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidHashingHandlerTypeError: invalid hashing handler type error.
        :raises InvalidHashingHandlerNameError: invalid hashing handler name error.
        :raises DuplicatedHashingHandlerError: duplicated hashing handler error.
        """

        if not isinstance(instance, AbstractHashingBase):
            raise InvalidHashingHandlerTypeError('Input parameter [{instance}] is '
                                                 'not an instance of [{base}].'
                                                 .format(instance=instance,
                                                         base=AbstractHashingBase))

        if instance.get_name() is None or len(instance.get_name().strip()) == 0:
            raise InvalidHashingHandlerNameError('Hashing handler [{instance}] '
                                                 'does not have a valid name.'
                                                 .format(instance=instance))

        # checking whether is there any registered instance with the same name.
        if instance.get_name() in self._hashing_handlers:
            replace = options.get('replace', False)

            if replace is not True:
                raise DuplicatedHashingHandlerError('There is another registered hashing '
                                                    'handler with name [{name}] but "replace" '
                                                    'option is not set, so handler '
                                                    '[{instance}] could not be registered.'
                                                    .format(name=instance.get_name(),
                                                            instance=instance))

            old_instance = self._hashing_handlers[instance.get_name()]
            print_warning('Hashing handler [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=old_instance, new_instance=instance))

        # registering new hashing handler.
        self._hashing_handlers[instance.get_name()] = instance

    def generate_hash(self, text, **options):
        """
        gets the hash of input text using a random or specified salt.

        :param str text: text to be hashed.

        :keyword str handler_name: handler name to be used for hash generation.
                                   if not provided, default handler from
                                   relevant configs will be used.

        :keyword bytes salt: salt to be used for hashing.
                             if not provided, a random salt will be generated
                             considering `salt_length` option.

        :keyword str internal_algorithm: internal algorithm to be used
                                         for hashing. if not provided,
                                         default value from relevant
                                         config will be used.

        :keyword int rounds: rounds to perform for generating hash.
                             if not provided, default value from
                             relevant config will be used.

        :keyword int salt_length: salt length to be used for hashing.
                                  if `salt` option is provided, then
                                  this value will be ignored.
                                  if not provided, default value from
                                  relevant config will be used.

        :keyword str prefix: prefix to be used for bcrypt hashing.

        :rtype: str
        """

        return self._get_hashing_handler(**options).generate_hash(text, **options)

    def is_match(self, text, full_hashed_value, **options):
        """
        gets a value indicating that given text's
        hash is identical to given full hashed value.

        :param str text: text to be hashed.
        :param str full_hashed_value: full hashed value to compare with.

        :rtype: bool
        """

        handler_name = self._extract_handler_name(full_hashed_value, **options)
        return self._get_hashing_handler(handler_name=handler_name).is_match(
            text, full_hashed_value, **options)

    def _get_hashing_handler(self, **options):
        """
        gets the specified hashing handler.

        :keyword str handler_name: handler name to get.
                                   if not provided, default handler from
                                   relevant configs will be used.

        :raises HashingHandlerNotFoundError: hashing handler not found error.

        :rtype: AbstractHashingBase
        """

        handler_name = options.get('handler_name', self._get_default_handler_name())
        if handler_name not in self._hashing_handlers.keys():
            raise HashingHandlerNotFoundError('Hashing handler [{name}] not found.'
                                              .format(name=handler_name))

        return self._hashing_handlers[handler_name]

    def _get_default_handler_name(self):
        """
        gets default hashing handler name from configs.

        :rtype: str
        """

        return config_services.get('security', 'hashing', 'default_hashing_handler')

    def _extract_handler_name(self, full_hashed_value, **options):
        """
        extracts the handler name of given full hashed value.

        :param str full_hashed_value: full hashed value to extract the handler name from.

        :raises InvalidHashError: invalid hash error.

        :rtype: str
        """

        if full_hashed_value.count(self._separator) < 2:
            raise InvalidHashError('Input hash value has an incorrect format.')

        items = full_hashed_value.split(self._separator, 2)
        return items[1]

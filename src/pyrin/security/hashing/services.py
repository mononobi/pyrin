# -*- coding: utf-8 -*-
"""
hashing services module.
"""

from pyrin.application.services import get_component
from pyrin.security.hashing import HashingPackage


def register_hashing_handler(instance, **options):
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

    return get_component(HashingPackage.COMPONENT_NAME).register_hashing_handler(instance,
                                                                                 **options)


def generate_hash(text, **options):
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

    return get_component(HashingPackage.COMPONENT_NAME).generate_hash(text, **options)


def is_match(text, full_hashed_value, **options):
    """
    gets a value indicating that given text's
    hash is identical to given full hashed value.

    :param str text: text to be hashed.
    :param str full_hashed_value: full hashed value to compare with.

    :rtype: bool
    """

    return get_component(HashingPackage.COMPONENT_NAME).is_match(text, full_hashed_value,
                                                                 **options)

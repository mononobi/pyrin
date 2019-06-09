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

    :param HashingBase instance: hashing handler to be registered.
                                 it must be an instance of HashingBase.

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


def generate_hash(handler_name, plain_text, salt, **options):
    """
    gets the hash of input plain text and salt using given handler.

    :param str handler_name: handler name to be used for hashing.
    :param str plain_text: text to be hashed.
    :param str salt: salt to append to plain text before hashing.

    :keyword int rounds: rounds to perform for generating hash.
                         if not provided, default value from
                         relevant config will be used.

    :rtype: str
    """

    return get_component(HashingPackage.COMPONENT_NAME).generate_hash(handler_name,
                                                                      plain_text,
                                                                      salt, **options)


def generate_salt(handler_name, **options):
    """
    generates a valid salt for the given handler and returns it.

    :param str handler_name: handler name to be used for salt generation.

    :keyword int length: length of generated salt.
                         some hashing handlers may not accept custom salt length,
                         so this value would be ignored on those handlers.

    :keyword int rounds: rounds to perform for generating hash.
                         if not provided, default value from
                         relevant config will be used.

    :rtype: str
    """

    return get_component(HashingPackage.COMPONENT_NAME).generate_salt(handler_name, **options)


def is_match(handler_name, plain_text, hashed_value):
    """
    gets a value indicating that given plain text's
    hash is identical to given hashed  using specified handler.

    :param str handler_name: handler name to be used for hash comparison.
    :param str plain_text: text to be hashed.
    :param str hashed_value: hashed value to compare with.

    :rtype: bool
    """

    return get_component(HashingPackage.COMPONENT_NAME).is_match(handler_name,
                                                                 plain_text, hashed_value)

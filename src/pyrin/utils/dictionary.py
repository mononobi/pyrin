# -*- coding: utf-8 -*-
"""
utils dictionary module.
"""
from operator import itemgetter

import pyrin.utils.string as string_utils

from pyrin.core.structs import DTO
from pyrin.utils.exceptions import InputNotCallableError, DictKeyPrefixIsNotProvidedError


def change_key_case(value, converter, **options):
    """
    returns a copy of input dict with all it's keys
    and nested keys cases modified using given converter.
    note that this only considers direct nested dicts, if there is a
    list that contains a dict as value, this method won't change that.

    :param dict value: dict to change it's keys cases.

    :param callable converter: a callable to use as case converter.
                               it should be a callable with a signature
                               similar to below example.
                               case_converter(input_dict).

    :raises InputNotCallableError: input not callable error.

    :rtype: dict
    """

    if not callable(converter):
        raise InputNotCallableError('Input parameter [{converter}] is not callable.'
                                    .format(converter=str(converter)))

    result_dict = DTO()
    for key, val in value.items():
        if isinstance(val, dict):
            val = change_key_case(val, converter, **options)
        result_dict[converter(key)] = val
    return result_dict


def make_key_upper(value):
    """
    returns a copy of input dict with all it's
    keys and nested keys cases made upper.
    note that this only considers direct nested dicts, if there is a
    list that contains a dict as value, this method won't change that.

    :param dict value: dict to make it's keys uppercase.

    :rtype: dict
    """

    return change_key_case(value, string_utils.upper)


def make_key_lower(value):
    """
    returns a copy of input dict with all it's
    keys and nested keys cases made lower.
    note that this only considers direct nested dicts, if there is a
    list that contains a dict as value, this method won't change that.

    :param dict value: dict to make it's keys lowercase.

    :rtype: dict
    """

    return change_key_case(value, string_utils.lower)


def remove_keys(value, prefix):
    """
    removes all keys from given dict which starting with given prefix and
    also those keys that their names are exactly like prefixed ones, but without prefix.
    for example: dict(name='some_name', value='value', __value='another_value')
    if prefix is double underscores `__` then this function will return a new dict
    result = dict(name='some_name') with just the name key.
    note that this function just loops through top level keys.

    :param dict value: dict to remove keys from it.
    :param str prefix: keys prefix that should be removed from dict.

    :raises DictKeyPrefixIsNotProvidedError: dict key prefix is not provided error.

    :rtype: dict
    """

    if prefix in (None, '') or prefix.isspace():
        raise DictKeyPrefixIsNotProvidedError('Dictionary key prefix must be provided '
                                              'to remove keys with such prefix.')

    prefix_length = len(prefix)
    prefixed_to_remove = [key for key in value.keys() if key.startswith(prefix)]
    original_to_remove = [key[prefix_length:] for key in prefixed_to_remove]
    prefixed_to_remove.extend(original_to_remove)
    result = DTO(**value)
    for key in prefixed_to_remove:
        result.pop(key, None)

    return result


def sort_by_value(value, reverse=False):
    """
    sorts a dictionary by its values.

    :param dict value: dict to be sorted.

    :param bool reverse: sort by descending value.
                         defaults to False if not provided.
    """

    return sorted(value.items(), key=lambda x: x[1], reverse=reverse)

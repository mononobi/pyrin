# -*- coding: utf-8 -*-
"""
utils test_dictionary module.
"""

import pyrin.utils.dictionary as dict_utils


def change_key_case(value, converter, **options):
    """
    returns a copy of input dict with all it's keys
    and nested keys cases modified using given converter.

    :param dict value: dict to change it's keys cases.

    :param callable converter: a callable to use as case converter.
                               it should be a callable with a signature
                               similar to below example.
                               case_converter(input_dict).

    :raises CoreTypeError: core type error.

    :rtype: dict
    """

    if not callable(converter):
        raise CoreTypeError('Input parameter [{converter}] is not callable.'
                            .format(converter=str(converter)))

    result_dict = DTO()
    for key, val in value.items():
        if isinstance(val, dict):
            val = change_key_case(val, converter, **options)
        result_dict[converter(key)] = val
    return result_dict


def test_change_key_case():
    """

    """


def make_key_upper(value):
    """
    returns a copy of input dict with all it's
    keys and nested keys cases made upper.

    :param dict value: dict to make it's keys uppercase.

    :rtype: dict
    """

    return change_key_case(value, string_utils.upper)


def make_key_lower(value):
    """
    returns a copy of input dict with all it's
    keys and nested keys cases made lower.

    :param dict value: dict to make it's keys lowercase.

    :rtype: dict
    """

    return change_key_case(value, string_utils.lower)

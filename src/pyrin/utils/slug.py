# -*- coding: utf-8 -*-
"""
utils slug module.
"""

import string
import random

import pyrin.utils.string as string_utils
import pyrin.utils.unique_id as uuid_utils


def get_slug(chars, length=6, case_convertor=string_utils.upper):
    """
    gets a random slug with given length.

    :param str chars: a string of characters to be used for slug generation.

    :param int length: length of generated slug.
                       defaults to `6` if not provided.

    :param function case_convertor: a callable to be used as case converter
                                    for slug. defaults to `string_utils.upper`
                                    if not provided.

    :rtype: str
    """

    slug = ''.join(random.choices(chars, k=length))
    if case_convertor is not None:
        slug = case_convertor(slug)

    return slug


def get_letter_slug(length=6, case_convertor=string_utils.upper):
    """
    gets a slug of only letters.

    :param int length: length of generated slug.
                       defaults to `6` if not provided.

    :param function case_convertor: a callable to be used as case converter
                                    for slug. defaults to `string_utils.upper`
                                    if not provided.

    :rtype: str
    """

    return get_slug(string.ascii_letters, length, case_convertor=case_convertor)


def get_digit_slug(length=6):
    """
    gets a slug of only digits.

    :param int length: length of generated slug.
                       defaults to `6` if not provided.

    :rtype: str
    """

    return get_slug(string.digits, length, case_convertor=None)


def get_complex_slug(length=6, case_convertor=string_utils.upper):
    """
    gets a slug of letters and digits.

    :param int length: length of generated slug.
                       defaults to `6` if not provided.

    :param function case_convertor: a callable to be used as case converter
                                    for slug. defaults to `string_utils.upper`
                                    if not provided.

    :rtype: str
    """

    return get_slug(string.ascii_letters + string.digits,
                    length, case_convertor=case_convertor)


def get_hex_slug(length=16, case_convertor=None):
    """
    gets a slug from a uuid as hex string.

    :param int length: length of generated slug.
                       defaults to `16` if not provided.
                       the maximum length is `32`.

    :param function case_convertor: a callable to be used as case converter
                                    for slug. defaults to None if not provided.

    :rtype: str
    """

    slug = uuid_utils.generate_uuid4().hex
    if case_convertor is not None:
        slug = case_convertor(slug)

    return slug[0:length]

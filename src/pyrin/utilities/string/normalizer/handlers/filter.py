# -*- coding: utf-8 -*-
"""
string normalizer handlers filter module.
"""

import re

import pyrin.utils.string as string_utils

from pyrin.utilities.string.normalizer.decorators import string_normalizer
from pyrin.utilities.string.normalizer.enumerations import NormalizerEnum
from pyrin.utilities.string.normalizer.handlers.base import StringNormalizerBase, \
    ReplaceNormalizerBase


@string_normalizer()
class FilterNormalizer(StringNormalizerBase):
    """
    filter normalizer class.

    this normalizer removes given list of values from string.
    """

    def __init__(self, **options):
        """
        initializes an instance of FilterNormalizer.
        """

        super().__init__(NormalizerEnum.FILTER, 430, **options)

    def _normalize(self, value, **options):
        """
        normalizes the given value.

        :param str value: value to be normalized.

        :keyword list[str] filters: values to be removed from string.
        :keyword bool ignore_case: filter matches in case-insensitive way.
                                   defaults to True if not provided.

        :returns: normalized value.
        :rtype: str
        """

        filters = options.get('filters')
        if filters is None:
            return value

        flags = re.IGNORECASE
        ignore_case = options.get('ignore_case', True)
        if ignore_case is False:
            flags = 0

        filters = string_utils.sort_by_length(filters, reverse=True)
        for item in filters:
            value = re.sub(item, '', value, flags=flags)

        return value


@string_normalizer()
class PersianSignFilterNormalizer(ReplaceNormalizerBase):
    """
    persian sign filter normalizer class.

    this normalizer removes all common persian signs from string.
    """

    def __init__(self, **options):
        """
        initializes an instance of PersianSignFilterNormalizer.
        """

        replace_map = {'،': None, '؛': None, 'ـ': None,
                       '٬': None, '٪': None, '؟': None}

        super().__init__(NormalizerEnum.PERSIAN_SIGN, 420, replace_map, **options)


@string_normalizer()
class LatinSignFilterNormalizer(ReplaceNormalizerBase):
    """
    latin sign filter normalizer class.

    this normalizer removes all common latin signs from string.
    """

    def __init__(self, **options):
        """
        initializes an instance of LatinSignFilterNormalizer.
        """

        replace_map = {',': None, '.': None, ':': None, ';': None, '-': None,
                       '+': None, '_': None, '`': None, '"': None, "'": None,
                       '@': None, '#': None, '%': None, '^': None, '*': None,
                       '$': None, '(': None, ')': None, '{': None, '}': None,
                       '|': None, '~': None, '?': None, '!': None, '/': None,
                       '\\': None, '<': None, '>': None, '[': None, ']': None}

        super().__init__(NormalizerEnum.LATIN_SIGN, 410, replace_map, **options)

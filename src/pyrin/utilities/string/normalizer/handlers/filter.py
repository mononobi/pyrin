# -*- coding: utf-8 -*-
"""
string normalizer handlers filter module.
"""

from pyrin.utilities.string.normalizer.decorators import string_normalizer
from pyrin.utilities.string.normalizer.enumerations import NormalizerEnum
from pyrin.utilities.string.normalizer.handlers.base import ReplaceNormalizerBase, \
    FilterNormalizerBase


@string_normalizer()
class FilterNormalizer(FilterNormalizerBase):
    """
    filter normalizer class.

    this normalizer will filter provided values from string.
    """

    def __init__(self, **options):
        """
        initializes an instance of FilterNormalizer.

        :keyword list[str] filters: values to be removed from string.

        :keyword dict filter_map: a dict of keys and values to be used
                                  for replacement.

        :note filters, filter_map: the `filters` value have precedence
                                   over `filter_map` value if they have
                                   common keys.

        :raises FiltersMustBeListError: filters must be list error.
        :raises FilterMapMustBeDictError: filter map must be dict error.
        """

        super().__init__(NormalizerEnum.FILTER, 430, **options)


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

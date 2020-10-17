# -*- coding: utf-8 -*-
"""
string normalizer handlers space module.
"""

from pyrin.utilities.string.normalizer.decorators import string_normalizer
from pyrin.utilities.string.normalizer.enumerations import NormalizerEnum
from pyrin.utilities.string.normalizer.handlers.base import StringNormalizerBase


@string_normalizer()
class SpaceNormalizer(StringNormalizerBase):
    """
    space normalizer class.

    this normalizer removes all spaces.
    """

    def __init__(self, **options):
        """
        initializes an instance of SpaceNormalizer.
        """

        super().__init__(NormalizerEnum.SPACE, 120, **options)

    def _normalize(self, value, **options):
        """
        normalizes the given value.

        :param str value: value to be normalized.

        :returns: normalized value.
        :rtype: str
        """

        return value.replace(' ', '')


@string_normalizer()
class DuplicateSpaceNormalizer(StringNormalizerBase):
    """
    duplicate space normalizer class.

    this normalizer replaces all duplicate spaces with a single one.
    """

    def __init__(self, **options):
        """
        initializes an instance of DuplicateSpaceNormalizer.
        """

        super().__init__(NormalizerEnum.DUPLICATE_SPACE, 110, **options)

    def _normalize(self, value, **options):
        """
        normalizes the given value.

        :param str value: value to be normalized.

        :returns: normalized value.
        :rtype: str
        """

        while '  ' in value:
            value = value.replace('  ', ' ')

        return value

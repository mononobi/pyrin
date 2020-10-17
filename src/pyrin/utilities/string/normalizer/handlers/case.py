# -*- coding: utf-8 -*-
"""
string normalizer handlers case module.
"""

from pyrin.utilities.string.normalizer.decorators import string_normalizer
from pyrin.utilities.string.normalizer.enumerations import NormalizerEnum
from pyrin.utilities.string.normalizer.handlers.base import StringNormalizerBase


@string_normalizer()
class LowercaseNormalizer(StringNormalizerBase):
    """
    lowercase normalizer class.

    this normalizer makes the string lowercase.
    """

    def __init__(self, **options):
        """
        initializes an instance of LowercaseNormalizer.
        """

        super().__init__(NormalizerEnum.LOWERCASE, 210, **options)

    def _normalize(self, value, **options):
        """
        normalizes the given value.

        :param str value: value to be normalized.

        :returns: normalized value.
        :rtype: str
        """

        return value.lower()


@string_normalizer()
class UppercaseNormalizer(StringNormalizerBase):
    """
    uppercase normalizer class.

    this normalizer makes the string uppercase.
    """

    def __init__(self, **options):
        """
        initializes an instance of UppercaseNormalizer.
        """

        super().__init__(NormalizerEnum.UPPERCASE, 230, **options)

    def _normalize(self, value, **options):
        """
        normalizes the given value.

        :param str value: value to be normalized.

        :returns: normalized value.
        :rtype: str
        """

        return value.upper()


@string_normalizer()
class TitleCaseNormalizer(StringNormalizerBase):
    """
    title case normalizer class.

    this normalizer makes the string title case.
    meaning that first letter of each word will be capitalized.
    """

    def __init__(self, **options):
        """
        initializes an instance of TitleCaseNormalizer.
        """

        super().__init__(NormalizerEnum.TITLE_CASE, 220, **options)

    def _normalize(self, value, **options):
        """
        normalizes the given value.

        :param str value: value to be normalized.

        :returns: normalized value.
        :rtype: str
        """

        return value.title()

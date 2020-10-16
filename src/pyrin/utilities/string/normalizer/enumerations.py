# -*- coding: utf-8 -*-
"""
string normalizer enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class NormalizerEnum(CoreEnum):
    """
    normalizer enum.
    """

    SPACE = 'space'
    DUPLICATE_SPACE = 'duplicate_space'
    LOWERCASE = 'lowercase'
    UPPERCASE = 'uppercase'
    TITLE_CASE = 'title_case'
    FILTER = 'filter'
    PERSIAN_SIGN = 'persian_sign'
    LATIN_SIGN = 'latin_sign'
    PERSIAN_NUMBER = 'persian_number'
    ARABIC_NUMBER = 'arabic_number'
    PERSIAN_LETTER = 'persian_letter'
    LATIN_LETTER = 'latin_letter'

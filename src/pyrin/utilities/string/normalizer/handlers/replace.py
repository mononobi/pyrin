# -*- coding: utf-8 -*-
"""
string normalizer handlers replace module.
"""

from pyrin.utilities.string.normalizer.decorators import string_normalizer
from pyrin.utilities.string.normalizer.enumerations import NormalizerEnum
from pyrin.utilities.string.normalizer.handlers.base import ReplaceNormalizerBase


@string_normalizer()
class PersianNumberNormalizer(ReplaceNormalizerBase):
    """
    persian number normalizer class.

    this normalizer replaces all persian numbers with latin numbers.
    """

    def __init__(self, **options):
        """
        initializes an instance of PersianNumberNormalizer.
        """

        replace_map = {'۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
                       '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'}

        super().__init__(NormalizerEnum.PERSIAN_NUMBER, 310, replace_map, **options)


@string_normalizer()
class ArabicNumberNormalizer(ReplaceNormalizerBase):
    """
    arabic number normalizer class.

    this normalizer replaces all arabic numbers with latin numbers.
    """

    def __init__(self, **options):
        """
        initializes an instance of ArabicNumberNormalizer.
        """

        replace_map = {'٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
                       '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'}

        super().__init__(NormalizerEnum.ARABIC_NUMBER, 320, replace_map, **options)


@string_normalizer()
class PersianLetterNormalizer(ReplaceNormalizerBase):
    """
    persian letter normalizer class.

    this normalizer replaces all non standard persian letters with standard versions.
    """

    def __init__(self, **options):
        """
        initializes an instance of PersianLetterNormalizer.
        """

        replace_map = {'ي': 'ی', 'ك': 'ک', 'إ': 'ا', 'أ': 'ا',
                       'ؤ': 'و', 'ۀ': 'ه', 'ة': 'ه', 'آ': 'ا'}

        super().__init__(NormalizerEnum.PERSIAN_LETTER, 330, replace_map, **options)


@string_normalizer()
class LatinLetterNormalizer(ReplaceNormalizerBase):
    """
    latin letter normalizer class.

    this normalizer replaces all latin letters with english versions.
    """

    def __init__(self, **options):
        """
        initializes an instance of LatinLetterNormalizer.
        """

        replace_map = {'ä': 'a', 'Ä': 'A', 'ë': 'e', 'Ë': 'E', 'ï': 'i',
                       'Ï': 'I', 'ö': 'o', 'Ö': 'O', 'ü': 'u', 'Ü': 'U',
                       'ÿ': 'y', 'Ÿ': 'Y', 'á': 'a', 'Á': 'A', 'ć': 'c',
                       'Ć': 'C', 'é': 'e', 'É': 'E', 'í': 'i', 'Í': 'I',
                       'ń': 'n', 'Ń': 'N', 'ó': 'o', 'Ó': 'O', 'ś': 's',
                       'Ś': 'S', 'ú': 'u', 'Ú': 'U', 'ý': 'y', 'Ý': 'Y',
                       'ź': 'z', 'Ź': 'Z', 'ő': 'o', 'Ő': 'O', 'ű': 'u',
                       'Ű': 'U', 'à': 'a', 'À': 'A', 'è': 'e', 'È': 'E',
                       'ì': 'i', 'Ì': 'I', 'ò': 'o', 'Ò': 'O', 'ù': 'u',
                       'Ù': 'U', 'â': 'a', 'Â': 'A', 'ê': 'e', 'Ê': 'E',
                       'î': 'i', 'Î': 'I', 'ô': 'o', 'Ô': 'O', 'û': 'u',
                       'Û': 'U', 'ã': 'a', 'Ã': 'A', 'ñ': 'n', 'Ñ': 'N',
                       'õ': 'o', 'Õ': 'O', 'č': 'c', 'Č': 'C', 'ď': 'd',
                       'Ď': 'D', 'ě': 'e', 'Ě': 'E', 'ǧ': 'g', 'Ǧ': 'G',
                       'ň': 'n', 'Ň': 'N', 'ř': 'r', 'Ř': 'R', 'š': 's',
                       'Š': 'S', 'ť': 't', 'Ť': 'T', 'ž': 'z', 'Ž': 'Z',
                       'đ': 'd', 'Đ': 'D'}

        super().__init__(NormalizerEnum.LATIN_LETTER, 340, replace_map, **options)

# -*- coding: utf-8 -*-
"""
string normalizer handlers exceptions module.
"""

from pyrin.core.exceptions import CoreException


class StringNormalizersException(CoreException):
    """
    string normalizers exception.
    """
    pass


class InvalidStringNormalizerNameError(StringNormalizersException):
    """
    invalid string normalizer name error.
    """
    pass


class InvalidStringNormalizerPriorityError(StringNormalizersException):
    """
    invalid string normalizer priority error.
    """
    pass

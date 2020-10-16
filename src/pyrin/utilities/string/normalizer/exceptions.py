# -*- coding: utf-8 -*-
"""
string normalizer exceptions module.
"""

from pyrin.core.exceptions import CoreException


class StringNormalizerManagerException(CoreException):
    """
    string normalizer manager exception.
    """
    pass


class InvalidStringNormalizerTypeError(StringNormalizerManagerException):
    """
    invalid string normalizer type error.
    """
    pass


class DuplicatedStringNormalizerError(StringNormalizerManagerException):
    """
    duplicated string normalizer error.
    """
    pass


class StringNormalizerDoesNotExistError(StringNormalizerManagerException):
    """
    string normalizer does not exist error.
    """
    pass

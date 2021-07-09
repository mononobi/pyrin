# -*- coding: utf-8 -*-
"""
swagger exceptions module.
"""

from pyrin.core.exceptions import CoreException


class SwaggerException(CoreException):
    """
    swagger exception.
    """
    pass


class InvalidTagTypeError(SwaggerException):
    """
    invalid tag type error.
    """
    pass


class DuplicatedTagError(SwaggerException):
    """
    duplicated tag error.
    """
    pass

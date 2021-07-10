# -*- coding: utf-8 -*-
"""
swagger tags exceptions module.
"""

from pyrin.core.exceptions import CoreException


class SwaggerTagsException(CoreException):
    """
    swagger tags exception.
    """
    pass


class TagNameIsRequiredError(SwaggerTagsException):
    """
    tag name is required error.
    """
    pass


class TagIsRequiredError(SwaggerTagsException):
    """
    tag is required error.
    """
    pass

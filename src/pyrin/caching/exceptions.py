# -*- coding: utf-8 -*-
"""
caching exceptions module.
"""


from pyrin.core.exceptions import CoreException


class CachingManagerException(CoreException):
    """
    caching manager exception.
    """
    pass


class NotBoundedToClassError(CachingManagerException):
    """
    not bounded to class error.
    """
    pass
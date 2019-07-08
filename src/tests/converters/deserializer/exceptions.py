# -*- coding: utf-8 -*-
"""
deserializer exceptions module.
"""

from pyrin.core.exceptions import CoreException


class DeserializerManagerException(CoreException):
    """
    deserializer manager exception.
    """
    pass


class InvalidDeserializerTypeError(DeserializerManagerException):
    """
    invalid deserializer type error.
    """
    pass


class DuplicatedDeserializerError(DeserializerManagerException):
    """
    duplicated deserializer error.
    """
    pass

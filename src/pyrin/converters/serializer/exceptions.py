# -*- coding: utf-8 -*-
"""
serializer exceptions module.
"""

from pyrin.core.exceptions import CoreException


class SerializerManagerException(CoreException):
    """
    serializer manager exception.
    """
    pass


class InvalidSerializerTypeError(SerializerManagerException):
    """
    invalid serializer type error.
    """
    pass


class DuplicatedSerializerError(SerializerManagerException):
    """
    duplicated serializer error.
    """
    pass

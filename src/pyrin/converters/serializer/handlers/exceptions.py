# -*- coding: utf-8 -*-
"""
serializer handlers exceptions module.
"""

from pyrin.core.exceptions import CoreException
from pyrin.database.model.exceptions import ColumnNotExistedError as BaseColumnNotExistedError


class SerializerHandlersException(CoreException):
    """
    serializer handlers exception.
    """
    pass


class ColumnNotExistedError(SerializerHandlersException, BaseColumnNotExistedError):
    """
    column not existed error.
    """
    pass

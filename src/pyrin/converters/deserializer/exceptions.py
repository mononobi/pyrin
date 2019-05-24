# -*- coding: utf-8 -*-
"""
deserializer exceptions module.
"""

from pyrin.exceptions import CoreTypeError, CoreKeyError


class InvalidDeserializerTypeError(CoreTypeError):
    """
    invalid deserializer type error.
    """
    pass


class DuplicatedDeserializerError(CoreKeyError):
    """
    duplicated deserializer error.
    """
    pass

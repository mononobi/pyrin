# -*- coding: utf-8 -*-
"""
encryption handlers exceptions module.
"""

from pyrin.core.exceptions import CoreValueError


class InvalidEncryptedValueError(CoreValueError):
    """
    invalid encrypted value error.
    """
    pass


class EncryptionHandlerMismatchError(CoreValueError):
    """
    encryption handler mismatch error.
    """
    pass

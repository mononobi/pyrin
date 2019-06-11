# -*- coding: utf-8 -*-
"""
security exceptions module.
"""

from pyrin.core.exceptions import CoreValueError


class InvalidPasswordError(CoreValueError):
    """
    invalid password error.
    """
    pass

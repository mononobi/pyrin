# -*- coding: utf-8 -*-
"""
security enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class TokenTypeEnum(CoreEnum):
    """
    token type enum.
    """

    ACCESS = 'access'
    REFRESH = 'refresh'

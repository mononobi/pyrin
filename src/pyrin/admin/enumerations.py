# -*- coding: utf-8 -*-
"""
admin enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class ClientTypeEnum(CoreEnum):
    """
    client type enum.
    """

    BOOLEAN = 'boolean'
    NUMERIC = 'numeric'
    DATE = 'date'
    DATETIME = 'datetime'
    TIME = 'time'

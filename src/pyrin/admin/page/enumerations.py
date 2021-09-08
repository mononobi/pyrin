# -*- coding: utf-8 -*-
"""
admin page enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class TableTypeEnum(CoreEnum):
    """
    table type enum.
    """

    DENSE = 'dense'
    DEFAULT = 'default'


class PaginationTypeEnum(CoreEnum):
    """
    pagination type enum.
    """

    NORMAL = 'normal'
    STEPPED = 'stepped'


class PaginationPositionEnum(CoreEnum):
    """
    pagination position enum.
    """

    TOP = 'top'
    BOTTOM = 'bottom'
    BOTH = 'both'

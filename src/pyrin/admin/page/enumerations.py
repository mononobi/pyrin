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


class FormatEnum(CoreEnum):
    """
    format enum.
    """

    NUMERIC = 'numeric'
    TWO_DIGIT = '2-digit'


class MonthFormatEnum(CoreEnum):
    """
    month format enum.
    """

    NUMERIC = 'numeric'
    TWO_DIGIT = '2-digit'
    LONG = 'long'
    SHORT = 'short'
    NARROW = 'narrow'


class HourCycleEnum(CoreEnum):
    """
    hour cycle enum.
    """

    H23 = 'h23'
    H24 = 'h24'
    H11 = 'h11'
    H12 = 'h12'


class ButtonTypeEnum(CoreEnum):
    """
    button type enum.
    """

    CONTAINED = 'contained'
    OUTLINED = 'outlined'
    TEXT = 'text'


class LinkTypeEnum(CoreEnum):
    """
    link type enum.
    """

    BUTTON = 'button'
    LINK = 'link'

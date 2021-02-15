# -*- coding: utf-8 -*-
"""
database enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class FKRestrictionEnum(CoreEnum):
    """
    fk restriction enum.
    """

    CASCADE = 'CASCADE'
    DELETE = 'DELETE'
    RESTRICT = 'RESTRICT'

# -*- coding: utf-8 -*-
"""
alembic enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class AlembicCLIHandlersEnum(CoreEnum):
    """
    alembic cli handlers enum.
    """

    ENABLE = 'alembic.enable'
    BRANCHES = 'branches'
    CURRENT = 'current'
    DOWNGRADE = 'downgrade'
    HEADS = 'heads'
    HISTORY = 'history'
    MERGE = 'merge'
    REVISION = 'revision'
    SHOW = 'show'
    STAMP = 'stamp'
    UPGRADE = 'upgrade'

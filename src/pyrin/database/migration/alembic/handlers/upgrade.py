# -*- coding: utf-8 -*-
"""
alembic handlers upgrade module.
"""

from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.enumerations import AlembicCLIHandlersEnum
from pyrin.database.migration.alembic.handlers.base import \
    AlembicUpgradeDowngradeCLIHandlerBase


@alembic_cli_handler()
class UpgradeCLIHandler(AlembicUpgradeDowngradeCLIHandlerBase):
    """
    upgrade cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of UpgradeCLIHandler.
        """

        super().__init__(AlembicCLIHandlersEnum.UPGRADE)

# -*- coding: utf-8 -*-
"""
database migration alembic handlers current module.
"""

from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.handlers.base import AlembicReportingCLIHandlerBase


@alembic_cli_handler()
class CurrentCLIHandler(AlembicReportingCLIHandlerBase):
    """
    current cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of CurrentCLIHandler.
        """

        super().__init__('current')

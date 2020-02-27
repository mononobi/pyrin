# -*- coding: utf-8 -*-
"""
database migration alembic handlers history module.
"""

from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.handlers.base import AlembicReportingCLIHandlerBase
from pyrin.database.migration.alembic.handlers.params import IndicateCurrentParamMixin, \
    RevisionRangeParamMixin


@alembic_cli_handler()
class HistoryCLIHandler(AlembicReportingCLIHandlerBase,
                        IndicateCurrentParamMixin, RevisionRangeParamMixin):
    """
    history cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of HistoryCLIHandler.
        """

        super().__init__('history')

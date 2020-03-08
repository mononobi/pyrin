# -*- coding: utf-8 -*-
"""
alembic handlers history module.
"""

from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.enumerations import AlembicCLIHandlersEnum
from pyrin.database.migration.alembic.handlers.base import AlembicReportingCLIHandlerBase
from pyrin.database.migration.alembic.handlers.params import IndicateCurrentParam, \
    RevisionRangeParam


@alembic_cli_handler()
class HistoryCLIHandler(AlembicReportingCLIHandlerBase):
    """
    history cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of HistoryCLIHandler.
        """

        super().__init__(AlembicCLIHandlersEnum.HISTORY)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([IndicateCurrentParam(), RevisionRangeParam()])
        return super()._inject_params(params)

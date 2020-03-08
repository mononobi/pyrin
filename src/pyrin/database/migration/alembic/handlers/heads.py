# -*- coding: utf-8 -*-
"""
alembic handlers heads module.
"""

from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.enumerations import AlembicCLIHandlersEnum
from pyrin.database.migration.alembic.handlers.base import AlembicReportingCLIHandlerBase
from pyrin.database.migration.alembic.handlers.params import ResolveDependenciesParam


@alembic_cli_handler()
class HeadsCLIHandler(AlembicReportingCLIHandlerBase):
    """
    heads cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of HeadsCLIHandler.
        """

        super().__init__(AlembicCLIHandlersEnum.HEADS)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.append(ResolveDependenciesParam())
        return super()._inject_params(params)

# -*- coding: utf-8 -*-
"""
alembic handlers stamp module.
"""

from pyrin.database.migration.alembic.enumerations import AlembicCLIHandlersEnum
from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase
from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.handlers.params import SQLParam, TagParam, \
    PurgeParam, RevisionsParam


@alembic_cli_handler()
class StampCLIHandler(AlembicCLIHandlerBase):
    """
    stamp cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of StampCLIHandler.
        """

        super().__init__(AlembicCLIHandlersEnum.STAMP)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([SQLParam(), TagParam(),
                       PurgeParam(), RevisionsParam()])

        return super()._inject_params(params)

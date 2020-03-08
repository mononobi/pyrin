# -*- coding: utf-8 -*-
"""
alembic handlers merge module.
"""

from pyrin.database.migration.alembic.enumerations import AlembicCLIHandlersEnum
from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase
from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.handlers.params import MessageParam, \
    BranchLabelParam, RevisionIDParam, RevisionsParam


@alembic_cli_handler()
class MergeCLIHandler(AlembicCLIHandlerBase):
    """
    merge cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of MergeCLIHandler.
        """

        super().__init__(AlembicCLIHandlersEnum.MERGE)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([MessageParam(), BranchLabelParam(),
                       RevisionIDParam(), RevisionsParam()])

        return super()._inject_params(params)

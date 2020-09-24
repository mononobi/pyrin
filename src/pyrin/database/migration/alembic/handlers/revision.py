# -*- coding: utf-8 -*-
"""
alembic handlers revision module.
"""

from pyrin.database.migration.alembic.enumerations import AlembicCLIHandlersEnum
from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase
from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.handlers.params import MessageParam, \
    AutoGenerateParam, SQLParam, HeadParam, SpliceParam, BranchLabelParam, \
    VersionPathParam, RevisionIDParam, DependsOnParam


@alembic_cli_handler()
class RevisionCLIHandler(AlembicCLIHandlerBase):
    """
    revision cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of RevisionCLIHandler.
        """

        super().__init__(AlembicCLIHandlersEnum.REVISION)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([MessageParam(), BranchLabelParam(),
                       RevisionIDParam(), SpliceParam(),
                       AutoGenerateParam(default=True),
                       HeadParam(), DependsOnParam(),
                       VersionPathParam(), SQLParam()])

        return super()._inject_params(params)

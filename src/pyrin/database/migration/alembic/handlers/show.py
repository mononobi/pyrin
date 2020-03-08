# -*- coding: utf-8 -*-
"""
alembic handlers show module.
"""

from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.enumerations import AlembicCLIHandlersEnum
from pyrin.database.migration.alembic.handlers.params import RevisionParam
from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase


@alembic_cli_handler()
class ShowCLIHandler(AlembicCLIHandlerBase):
    """
    show cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of ShowCLIHandler.
        """

        super().__init__(AlembicCLIHandlersEnum.SHOW)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.append(RevisionParam())
        return super()._inject_params(params)

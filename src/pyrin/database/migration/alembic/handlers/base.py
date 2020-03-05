# -*- coding: utf-8 -*-
"""
alembic handlers base module.
"""

from pyrin.cli.params import VerboseParam
from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase
from pyrin.database.migration.alembic.handlers.params import SQLParam, TagParam, RevisionParam


class AlembicUpgradeDowngradeCLIHandlerBase(AlembicCLIHandlerBase):
    """
    alembic upgrade downgrade cli handler base class.

    all alembic upgrade or downgrade cli handlers must be subclassed from this.
    """

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([SQLParam(), TagParam(), RevisionParam()])
        return super()._inject_params(params)


class AlembicReportingCLIHandlerBase(AlembicCLIHandlerBase):
    """
    alembic reporting cli handler base class.

    all alembic reporting cli handlers must be subclassed from this.
    """

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.append(VerboseParam())
        return super()._inject_params(params)

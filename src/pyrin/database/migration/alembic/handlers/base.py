# -*- coding: utf-8 -*-
"""
database migration alembic handlers base module.
"""

from pyrin.cli.params import VerboseParamMixin
from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase
from pyrin.database.migration.alembic.handlers.params import SQLParamMixin, TagParamMixin, \
    RevisionParamMixin


class AlembicUpgradeDowngradeCLIHandlerBase(SQLParamMixin, TagParamMixin,
                                            RevisionParamMixin):
    """
    alembic upgrade downgrade cli handler base class.
    all alembic upgrade or downgrade cli handlers must be subclassed from this.
    """
    pass


class AlembicReportingCLIHandlerBase(AlembicCLIHandlerBase, VerboseParamMixin):
    """
    alembic reporting cli handler base class.
    all alembic reporting cli handlers must be subclassed from this.
    """
    pass

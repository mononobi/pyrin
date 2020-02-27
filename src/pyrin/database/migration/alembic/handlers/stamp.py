# -*- coding: utf-8 -*-
"""
database migration alembic handlers stamp module.
"""

from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.handlers.params import SQLParamMixin, TagParamMixin, \
    PurgeParamMixin, RevisionsParamMixin


@alembic_cli_handler()
class StampCLIHandler(SQLParamMixin, TagParamMixin,
                      PurgeParamMixin, RevisionsParamMixin):
    """
    stamp cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of StampCLIHandler.
        """

        super().__init__('stamp')

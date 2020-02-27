# -*- coding: utf-8 -*-
"""
database migration alembic handlers merge module.
"""

from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.handlers.params import MessageParamMixin, \
    BranchLabelParamMixin, RevisionIDParamMixin, RevisionsParamMixin


@alembic_cli_handler()
class MergeCLIHandler(MessageParamMixin, BranchLabelParamMixin,
                      RevisionIDParamMixin, RevisionsParamMixin):
    """
    merge cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of MergeCLIHandler.
        """

        super().__init__('merge')

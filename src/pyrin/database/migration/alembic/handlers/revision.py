# -*- coding: utf-8 -*-
"""
database migration alembic handlers revision module.
"""

from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.handlers.params import MessageParamMixin, \
    AutoGenerateParamMixin, SQLParamMixin, HeadParamMixin, SpliceParamMixin, \
    BranchLabelParamMixin, VersionPathParamMixin, RevisionIDParamMixin, DependsOnParamMixin


@alembic_cli_handler()
class RevisionCLIHandler(MessageParamMixin, AutoGenerateParamMixin,
                         SQLParamMixin, HeadParamMixin, SpliceParamMixin,
                         BranchLabelParamMixin, VersionPathParamMixin,
                         RevisionIDParamMixin, DependsOnParamMixin):
    """
    revision cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of RevisionCLIHandler.
        """

        super().__init__('revision')

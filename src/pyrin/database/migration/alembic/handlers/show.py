# -*- coding: utf-8 -*-
"""
database migration alembic handlers show module.
"""

from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.handlers.params import RevisionParamMixin


@alembic_cli_handler()
class ShowCLIHandler(RevisionParamMixin):
    """
    show cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of ShowCLIHandler.
        """

        super().__init__('show')

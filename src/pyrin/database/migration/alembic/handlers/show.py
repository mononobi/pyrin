# -*- coding: utf-8 -*-
"""
database migration alembic handlers show module.
"""

from pyrin.cli.interface import CLIHandlerOptionsMetadata
from pyrin.database.migration.alembic.decorators import alembic_cli_handler
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

        super().__init__('show')

    def _generate_custom_cli_handler_options_metadata(self):
        """
        generates custom cli handler options metadata.

        :rtype: list[CLIHandlerOptionsMetadata]
        """

        revision = CLIHandlerOptionsMetadata('revision', None)
        options = [revision]

        return options

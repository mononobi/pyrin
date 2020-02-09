# -*- coding: utf-8 -*-
"""
database migration alembic handlers heads module.
"""

from pyrin.cli.interface import CLIHandlerOptionsMetadata
from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.handlers.base import AlembicReportingCLIHandlerBase


@alembic_cli_handler()
class HeadsCLIHandler(AlembicReportingCLIHandlerBase):
    """
    heads cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of HeadsCLIHandler.
        """

        super().__init__('heads')

    def _generate_custom_cli_handler_options_metadata(self):
        """
        generates custom cli handler options metadata.

        :rtype: list[CLIHandlerOptionsMetadata]
        """

        resolve_dependencies = CLIHandlerOptionsMetadata('resolve_dependencies', None,
                                                         {True: '--resolve-dependencies',
                                                          False: None})
        options = [resolve_dependencies]

        return options

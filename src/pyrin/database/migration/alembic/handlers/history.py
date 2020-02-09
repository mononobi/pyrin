# -*- coding: utf-8 -*-
"""
database migration alembic handlers history module.
"""

from pyrin.cli.interface import CLIHandlerOptionsMetadata
from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.handlers.base import AlembicReportingCLIHandlerBase


@alembic_cli_handler()
class HistoryCLIHandler(AlembicReportingCLIHandlerBase):
    """
    history cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of HistoryCLIHandler.
        """

        super().__init__('history')

    def _generate_custom_cli_handler_options_metadata(self):
        """
        generates custom cli handler options metadata.

        :rtype: list[CLIHandlerOptionsMetadata]
        """

        indicate_current = CLIHandlerOptionsMetadata('indicate_current', None,
                                                     {True: '--indicate-current',
                                                      False: None})
        revision_range = CLIHandlerOptionsMetadata('revision_range', '--rev-range')

        options = [indicate_current, revision_range]

        return options

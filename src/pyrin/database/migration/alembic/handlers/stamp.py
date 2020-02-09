# -*- coding: utf-8 -*-
"""
database migration alembic handlers stamp module.
"""

from pyrin.cli.interface import CLIHandlerOptionsMetadata
from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase


@alembic_cli_handler()
class StampCLIHandler(AlembicCLIHandlerBase):
    """
    stamp cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of StampCLIHandler.
        """

        super().__init__('stamp')

    def _generate_custom_cli_handler_options_metadata(self):
        """
        generates custom cli handler options metadata.

        :rtype: list[CLIHandlerOptionsMetadata]
        """

        sql = CLIHandlerOptionsMetadata('sql', None, {True: '--sql', False: None})
        tag = CLIHandlerOptionsMetadata('tag', '--tag')
        purge = CLIHandlerOptionsMetadata('purge', None, {True: '--purge', False: None})
        revisions = CLIHandlerOptionsMetadata('revisions', None)

        options = [sql, tag, purge, revisions]

        return options

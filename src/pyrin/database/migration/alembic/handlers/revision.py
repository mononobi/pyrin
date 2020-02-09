# -*- coding: utf-8 -*-
"""
database migration alembic handlers revision module.
"""

from pyrin.cli.interface import CLIHandlerOptionsMetadata
from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase


@alembic_cli_handler()
class RevisionCLIHandler(AlembicCLIHandlerBase):
    """
    revision cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of RevisionCLIHandler.
        """

        super().__init__('revision')

    def _generate_custom_cli_handler_options_metadata(self):
        """
        generates custom cli handler options metadata.

        :rtype: list[CLIHandlerOptionsMetadata]
        """

        message = CLIHandlerOptionsMetadata('message', '--message')
        autogenerate = CLIHandlerOptionsMetadata('autogenerate', None,
                                                 {True: '--autogenerate', False: None})
        sql = CLIHandlerOptionsMetadata('sql', None, {True: '--sql', False: None})
        head = CLIHandlerOptionsMetadata('head', '--head')
        splice = CLIHandlerOptionsMetadata('splice', None, {True: '--splice', False: None})
        branch_label = CLIHandlerOptionsMetadata('branch_label', '--branch-label')
        version_path = CLIHandlerOptionsMetadata('version_path', '--version-path')
        revision_id = CLIHandlerOptionsMetadata('revision_id', '--rev-id')
        depends_on = CLIHandlerOptionsMetadata('depends_on', '--depends-on')

        options = [message, autogenerate, sql,
                   head, splice, branch_label,
                   version_path, revision_id, depends_on]

        return options

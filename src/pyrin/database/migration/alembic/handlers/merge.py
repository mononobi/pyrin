# -*- coding: utf-8 -*-
"""
database migration alembic handlers merge module.
"""

from pyrin.cli.interface import CLIHandlerOptionsMetadata
from pyrin.database.migration.alembic.decorators import alembic_cli_handler
from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase


@alembic_cli_handler()
class MergeCLIHandler(AlembicCLIHandlerBase):
    """
    merge cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of MergeCLIHandler.
        """

        super().__init__('merge')

    def _generate_custom_cli_handler_options_metadata(self):
        """
        generates custom cli handler options metadata.

        :rtype: list[CLIHandlerOptionsMetadata]
        """

        message = CLIHandlerOptionsMetadata('message', '--message')
        branch_label = CLIHandlerOptionsMetadata('branch_label', '--branch-label')
        revision_id = CLIHandlerOptionsMetadata('revision_id', '--rev-id')
        revisions = CLIHandlerOptionsMetadata('revisions', None)

        options = [message, branch_label, revision_id, revisions]

        return options

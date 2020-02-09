# -*- coding: utf-8 -*-
"""
database migration alembic handlers base module.
"""

from pyrin.cli.interface import CLIHandlerOptionsMetadata
from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase


class AlembicReportingCLIHandlerBase(AlembicCLIHandlerBase):
    """
    alembic reporting cli handler base class.
    all alembic reporting cli handlers must be subclassed from this.
    """

    def _generate_common_cli_handler_options_metadata(self):
        """
        generates common cli handler options metadata.

        :rtype: list[CLIHandlerOptionsMetadata]
        """

        common_options = super()._generate_common_cli_handler_options_metadata()
        verbose = CLIHandlerOptionsMetadata('verbose', None, {True: '--verbose', False: None})
        common_options.extend([verbose])

        return common_options


class AlembicUpgradeDowngradeCLIHandlerBase(AlembicCLIHandlerBase):
    """
    alembic upgrade downgrade cli handler base class.
    all alembic upgrade or downgrade cli handlers must be subclassed from this.
    """

    def _generate_common_cli_handler_options_metadata(self):
        """
        generates common cli handler options metadata.

        :rtype: list[CLIHandlerOptionsMetadata]
        """

        common_options = super()._generate_common_cli_handler_options_metadata()
        sql = CLIHandlerOptionsMetadata('sql', None, {True: '--sql', False: None})
        tag = CLIHandlerOptionsMetadata('tag', '--tag')
        revision = CLIHandlerOptionsMetadata('revision', None)
        common_options.extend([sql, tag, revision])

        return common_options

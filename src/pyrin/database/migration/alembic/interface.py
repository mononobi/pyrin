# -*- coding: utf-8 -*-
"""
database migration alembic interface module.
"""

import pyrin.configuration.services as config_services

from pyrin.cli.interface import CLIHandlerBase, CLIHandlerOptionsMetadata
from pyrin.database.migration.alembic import DatabaseMigrationAlembicPackage


class AlembicCLIHandlerBase(CLIHandlerBase):
    """
    alembic cli handler base class.
    all alembic cli handlers must be subclassed from this.
    """

    def __init__(self, name):
        """
        initializes an instance of AlembicCLIHandlerBase.

        :param str name: the handler name that should be registered
                         with. this name must be the exact name that
                         this handler must emmit to cli.
        """

        super().__init__(name)
        self._config_file_path = config_services.get_file_path(
            DatabaseMigrationAlembicPackage.ALEMBIC_CONFIG_STORE)

    def _inject_common_cli_options(self, commands):
        """
        injecting some common cli options into the given list.

        :param list commands: a list of all commands and their
                              values to be sent to cli command.
        """

        bounded_options = ['alembic', '-c', self._config_file_path]
        for i in range(len(bounded_options)):
            commands.insert(i, bounded_options[i])

    def _generate_common_cli_handler_options_metadata(self):
        """
        generates common cli handler options metadata.

        :rtype: list[CLIHandlerOptionsMetadata]
        """

        help_option = CLIHandlerOptionsMetadata('help', None, {True: '--help', False: None})

        options = [help_option]

        return options

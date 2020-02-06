# -*- coding: utf-8 -*-
"""
database migration alembic handlers base module.
"""

import pyrin.configuration.services as config_services

from pyrin.cli.interface import CLIHandlerBase
from pyrin.database.migration.alembic.handlers import DatabaseMigrationAlembicHandlersPackage


class AlembicCLIHandlerBase(CLIHandlerBase):
    """
    alembic cli handler base class.
    all alembic cli handlers must be subclassed from this.
    """

    def __init__(self):
        """
        initializes an instance of AlembicCLIHandlerBase.
        """

        super().__init__()
        self._config_file_path = config_services.get_file_path(
            DatabaseMigrationAlembicHandlersPackage.ALEMBIC_CONFIG_STORE)

    def _inject_common_cli_options(self, commands):
        """
        injecting some common cli options into the given list.

        :param list commands: a list of all commands and their
                              values to be sent to cli command.
        """
        bounded_options = ['alembic', '-c', self._config_file_path]
        for i in range(len(bounded_options)):
            commands.insert(i, bounded_options[i])

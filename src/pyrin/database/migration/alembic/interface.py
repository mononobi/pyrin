# -*- coding: utf-8 -*-
"""
database migration alembic interface module.
"""

import pyrin.configuration.services as config_services

from pyrin.cli.params import HelpParamMixin
from pyrin.database.migration.alembic import DatabaseMigrationAlembicPackage


class AlembicCLIHandlerBase(HelpParamMixin):
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
            DatabaseMigrationAlembicPackage.CONFIG_STORE_NAMES[0])

    def _get_common_cli_options(self):
        """
        gets the list of common cli options.

        :rtype: list
        """

        return ['alembic', '-c', self._config_file_path]

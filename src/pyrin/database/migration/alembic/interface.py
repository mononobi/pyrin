# -*- coding: utf-8 -*-
"""
alembic interface module.
"""

import pyrin.configuration.services as config_services
import pyrin.database.migration.alembic.services as alembic_services

from pyrin.cli.base import CLIHandlerBase
from pyrin.cli.params import CLIParamBase


class AlembicCLIParamBase(CLIParamBase):
    """
    alembic cli param base class.

    all alembic cli param classes must be subclassed from this.
    """
    pass


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
        package = alembic_services.get_package_class()
        self._config_file_path = config_services.get_file_path(package.CONFIG_STORE_NAMES[0])

    def _get_common_cli_options(self):
        """
        gets the list of common cli options.

        :rtype: list
        """

        return ['alembic', '-c', self._config_file_path]

# -*- coding: utf-8 -*-
"""
database migration alembic package.
"""

import pyrin.application.services as application_services

from pyrin.core.context import DTO
from pyrin.packaging.base import Package


class DatabaseMigrationAlembicPackage(Package):
    """
    database migration alembic package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'database.migration.alembic.component'
    CONFIG_STORE_NAMES = ['alembic']

    @property
    def config_store_defaults(self):
        """
        gets config store default values that should
        be sent to config parser for interpolation.
        this method is intended to be overridden by subclasses.

        :returns: Union[dict, None]
        :rtype: dict
        """

        return DTO(script_location=application_services.get_migrations_path())

# -*- coding: utf-8 -*-
"""
database migration alembic package.
"""

from pyrin.packaging.context import Package


class DatabaseMigrationAlembicPackage(Package):
    """
    database migration alembic package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'database.migration.alembic.component'
    ALEMBIC_CONFIG_STORE = 'alembic'

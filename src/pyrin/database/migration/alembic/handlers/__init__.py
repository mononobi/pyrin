# -*- coding: utf-8 -*-
"""
database migration alembic handlers module.
"""

from pyrin.packaging.context import Package


class DatabaseMigrationAlembicHandlersPackage(Package):
    """
    database migration alembic handlers package class.
    """

    NAME = __name__
    ALEMBIC_CONFIG_STORE = 'alembic'

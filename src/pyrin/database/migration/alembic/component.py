# -*- coding: utf-8 -*-
"""
database migration alembic component module.
"""

from pyrin.application.decorators import component
from pyrin.database.migration.alembic import DatabaseMigrationAlembicPackage
from pyrin.database.migration.alembic.manager import DatabaseMigrationAlembicManager
from pyrin.application.context import Component


@component(DatabaseMigrationAlembicPackage.COMPONENT_NAME)
class DatabaseMigrationAlembicComponent(Component, DatabaseMigrationAlembicManager):
    """
    database migration alembic component class.
    """
    pass

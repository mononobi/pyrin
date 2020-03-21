# -*- coding: utf-8 -*-
"""
database migration component module.
"""

from pyrin.application.decorators import component
from pyrin.database.migration import DatabaseMigrationPackage
from pyrin.database.migration.manager import DatabaseMigrationManager
from pyrin.application.structs import Component


@component(DatabaseMigrationPackage.COMPONENT_NAME)
class DatabaseMigrationComponent(Component, DatabaseMigrationManager):
    """
    database migration component class.
    """
    pass

# -*- coding: utf-8 -*-
"""
database migration alembic services module.
"""

from pyrin.application.services import get_component
from pyrin.database.migration.alembic import DatabaseMigrationAlembicPackage


def create_all():
    """
    creates all entities on database engine.
    """

    return get_component(DatabaseMigrationAlembicPackage.COMPONENT_NAME).create_all()

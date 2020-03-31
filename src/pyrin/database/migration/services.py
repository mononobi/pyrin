# -*- coding: utf-8 -*-
"""
database migration services module.
"""

from pyrin.application.services import get_component
from pyrin.database.migration import DatabaseMigrationPackage


def create_all():
    """
    creates all entities on database engine.
    """

    return get_component(DatabaseMigrationPackage.COMPONENT_NAME).create_all()


def drop_all():
    """
    drops all entities on database engine.
    """

    return get_component(DatabaseMigrationPackage.COMPONENT_NAME).drop_all()


def get_connection_urls():
    """
    gets all database connection urls for each engine.

    it gets the values from active section of each store.
    in case of sqlite usage, all urls will be made absolute.

    :returns: dict[str bind_name: str connection_url]
    :rtype: dict
    """

    return get_component(DatabaseMigrationPackage.COMPONENT_NAME).get_connection_urls()


def get_bind_name_to_metadata_map():
    """
    gets bind name to metadata map.

    :returns: dict[str bind_name: MetaData metadata]
    :rtype: dict
    """

    return get_component(DatabaseMigrationPackage.COMPONENT_NAME).get_bind_name_to_metadata_map()


def configure_migration_data():
    """
    configures the required data for any migration.
    """

    return get_component(DatabaseMigrationPackage.COMPONENT_NAME).configure_migration_data()


def rebuild_schema():
    """
    rebuilds database schema based on database and environment config store values.

    this will occur only if application is not in scripting mode.
    """

    return get_component(DatabaseMigrationPackage.COMPONENT_NAME).rebuild_schema()

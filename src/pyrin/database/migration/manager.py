# -*- coding: utf-8 -*-
"""
database migration manager module.
"""

import pyrin.database.services as database_services
import pyrin.configuration.services as config_services

from pyrin.core.context import DTO, Manager
from pyrin.database.migration.adapters import MetaDataAdapter
from pyrin.database.model.base import CoreEntity


class DatabaseMigrationManager(Manager):
    """
    database migration manager class.
    """

    def __init__(self):
        """
        initializes an instance of DatabaseMigrationManager.
        """

        super().__init__()

        # a dictionary containing engine to tables map for all tables.
        # in the form of: {Engine engine: list[Table] tables}
        self._engine_to_table_map = DTO()

        # a dictionary containing bind name to metadata map. note that each metadata
        # only contains tables that should be created on relevant bounded engine.
        # the default engine is added with 'default' key.
        # in the form of: {str bind_name: MataDataAdapter metadata}
        self._bind_name_to_metadata_map = DTO()

    def create_all(self):
        """
        creates all entities on database engine.
        """

        for engine, tables in self._engine_to_table_map.items():
            if tables is not None and len(tables) > 0:
                CoreEntity.metadata.create_all(engine, tables)

    def drop_all(self):
        """
        drops all entities on database engine.
        """

        for engine, tables in self._engine_to_table_map.items():
            if tables is not None and len(tables) > 0:
                CoreEntity.metadata.drop_all(engine, tables)

    def _map_engine_to_table(self):
        """
        maps all engines to relevant tables.
        """

        all_tables = DTO(**CoreEntity.metadata.tables)
        for entity, engine in database_services.get_entity_to_engine_map().items():
            if engine not in self._engine_to_table_map:
                self._engine_to_table_map[engine] = []

            self._engine_to_table_map[engine].append(all_tables.pop(entity.table_fullname()))
            self._bind_to_metadata(engine, self._engine_to_table_map[engine])

        # all remaining tables are associated with default engine.
        if len(all_tables) > 0:
            self._engine_to_table_map[database_services.get_engine()] = list(all_tables.values())
            self._bind_to_metadata(database_services.get_engine(),
                                   self._engine_to_table_map[database_services.get_engine()])

    def get_connection_urls(self):
        """
        gets all databases connection urls from config store.
        it gets the values from active section of each store.

        :returns: dict(str bind_name: str connection_url)
        :rtype: dict
        """

        connections = DTO()
        connections['default'] = config_services.get_active('database', 'sqlalchemy_url')
        binds = config_services.get_active_section('database.binds')
        connections.update(**binds)

        return connections

    def _bind_to_metadata(self, engine, tables):
        """
        binds given engine to a metadata representing the given tables.

        :param Engine engine: engine object.
        :param list[Table] tables: tables to be added to a metadata.
        """

        bounded_engines = database_services.get_bounded_engines()
        bind_name = None
        for key, value in bounded_engines.items():
            if engine == value:
                bind_name = key
                break

        if bind_name is None and engine == database_services.get_engine():
            bind_name = 'default'
        elif bind_name is None and engine != database_services.get_engine():
            raise

        metadata = MetaDataAdapter(CoreEntity.metadata, tables)
        self._bind_name_to_metadata_map[bind_name] = metadata

    def get_bind_name_to_metadata_map(self):
        """
        gets bind name to metadata map.

        :returns: dict(str bind_name: MetaDataAdapter metadata)
        :rtype: dict
        """

        return self._bind_name_to_metadata_map

    def configure_migration_data(self):
        """
        configures the required data for any migration.
        """

        self._map_engine_to_table()

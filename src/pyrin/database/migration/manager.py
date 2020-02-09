# -*- coding: utf-8 -*-
"""
database migration manager module.
"""

from os import path

from sqlalchemy import MetaData

import pyrin.database.services as database_services
import pyrin.configuration.services as config_services
import pyrin.application.services as application_services

from pyrin.core.context import DTO, Manager
from pyrin.database.migration.exceptions import EngineBindNameNotFoundError
from pyrin.database.model.base import CoreEntity


class DatabaseMigrationManager(Manager):
    """
    database migration manager class.
    """

    DEFAULT_ENGINE_NAME = 'default'

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

        # all remaining tables are associated with default engine.
        if len(all_tables) > 0:
            self._engine_to_table_map[database_services.get_default_engine()] = \
                list(all_tables.values())

    def get_connection_urls(self):
        """
        gets all databases connection urls from config store.
        it gets the values from active section of each store.
        in case of sqlite usage, all urls will be made absolute.

        :returns: dict(str bind_name: str connection_url)
        :rtype: dict
        """

        connections = DTO()
        connections[self.DEFAULT_ENGINE_NAME] = config_services.get_active('database',
                                                                           'sqlalchemy_url')
        binds = config_services.get_active_section('database.binds')
        connections.update(**binds)

        for name, url in connections.items():
            connections[name] = self._get_absolute_connection_url(url)

        return connections

    def _map_bind_to_metadata(self):
        """
        maps bind names of different engines to a
        metadata representing the related tables.
        """

        for engine, tables in self._engine_to_table_map.items():
            bounded_engines = database_services.get_bounded_engines()
            bind_name_map = None
            for bind_name, bounded_engine in bounded_engines.items():
                if engine == bounded_engine:
                    bind_name_map = bind_name
                    break

            default_engine = database_services.get_default_engine()
            if bind_name_map is None and engine == default_engine:
                bind_name_map = self.DEFAULT_ENGINE_NAME
            elif bind_name_map is None and engine != default_engine:
                raise EngineBindNameNotFoundError('Could not find any bind name '
                                                  'for database engine [{name}].'
                                                  .format(name=str(engine)))

            self._bind_name_to_metadata_map[bind_name_map] = self._add_to_metadata(tables)

    def get_bind_name_to_metadata_map(self):
        """
        gets bind name to metadata map.

        :returns: dict(str bind_name: MetaData metadata)
        :rtype: dict
        """

        return self._bind_name_to_metadata_map

    def _add_to_metadata(self, tables):
        """
        adds given tables into a metadata and returns it.

        :param list[Tables] tables: tables to be added into metadata.

        :rtype: MetaData
        """

        metadata = MetaData()
        for table in tables:
            table.tometadata(metadata)

        return metadata

    def configure_migration_data(self):
        """
        configures the required data for any migration.
        """

        self._map_engine_to_table()
        self._map_bind_to_metadata()

    def _get_absolute_connection_url(self, connection_url):
        """
        gets absolute path of given connection string if required.
        it is only required when sqlite is in use.

        :param str connection_url: connection url.

        :rtype: str
        """

        if connection_url is None or 'sqlite' not in connection_url.lower() or \
                connection_url.lower().startswith('sqlite:////') or \
                'sqlite:///:memory:' in connection_url.lower():
            return connection_url

        root_path = application_services.get_application_root_path()
        url = connection_url.replace('sqlite:///', '')
        full_path = path.join(root_path, url)
        absolute_path = path.abspath(full_path)

        return 'sqlite:///{absolute_path}'.format(absolute_path=absolute_path)

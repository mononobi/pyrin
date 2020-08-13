# -*- coding: utf-8 -*-
"""
database migration manager module.
"""

from os import path

from sqlalchemy import MetaData

import pyrin.database.services as database_services
import pyrin.configuration.services as config_services
import pyrin.application.services as application_services
import pyrin.database.model.services as model_services

from pyrin.core.structs import DTO, Manager
from pyrin.database.migration import DatabaseMigrationPackage
from pyrin.database.migration.exceptions import EngineBindNameNotFoundError
from pyrin.utils.custom_print import print_warning, print_info


class DatabaseMigrationManager(Manager):
    """
    database migration manager class.
    """

    package_class = DatabaseMigrationPackage

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
                model_services.get_declarative_base().metadata.create_all(engine, tables)

    def drop_all(self):
        """
        drops all entities on database engine.
        """

        for engine, tables in self._engine_to_table_map.items():
            if tables is not None and len(tables) > 0:
                model_services.get_declarative_base().metadata.drop_all(engine, tables)

    def _map_engine_to_table(self):
        """
        maps all engines to relevant tables.
        """

        all_tables = DTO(**model_services.get_declarative_base().metadata.tables)
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
        gets all database connection urls for each engine.

        it gets the values from active section of each store.
        in case of sqlite usage, all urls will be made absolute.

        :returns: dict[str bind_name: str connection_url]
        :rtype: dict
        """

        prefix = database_services.get_configs_prefix()
        url_key = '{prefix}url'.format(prefix=prefix)
        connections = DTO()
        connections[database_services.get_default_database_name()] = \
            self._get_absolute_connection_url(config_services.get_active('database', url_key))

        for bind_name in self.get_bind_name_to_metadata_map():
            if bind_name != database_services.get_default_database_name():
                section_name = database_services.get_bind_config_section_name(bind_name)
                connections[bind_name] = self._get_absolute_connection_url(
                    config_services.get('database.binds', section_name, url_key))

        return connections

    def _map_bind_to_metadata(self):
        """
        maps bind names of different engines to a metadata representing the related tables.
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
                bind_name_map = database_services.get_default_database_name()
            elif bind_name_map is None and engine != default_engine:
                raise EngineBindNameNotFoundError('Could not find any bind name '
                                                  'for database engine [{name}].'
                                                  .format(name=str(engine)))

            self._bind_name_to_metadata_map[bind_name_map] = self._add_to_metadata(tables)

    def get_bind_name_to_metadata_map(self):
        """
        gets bind name to metadata map.

        :returns: dict[str bind_name: MetaData metadata]
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
                'sqlite:///:memory:' in connection_url.lower() or \
                connection_url == 'sqlite:///':
            return connection_url

        root_path = application_services.get_working_directory()
        url = connection_url.replace('sqlite:///', '')
        full_path = path.join(root_path, url)
        absolute_path = path.abspath(full_path)

        return 'sqlite:///{absolute_path}'.format(absolute_path=absolute_path)

    def rebuild_schema(self):
        """
        rebuilds database schema based on database and environment config store values.

        this will occur only if application is not in scripting mode.
        """

        if application_services.is_scripting_mode() is False:
            if config_services.get_active('database', 'drop_on_startup') is True:
                environment = config_services.get_active('environment', 'env')
                debug = config_services.get_active('environment', 'debug')
                unit_testing = config_services.get_active('environment', 'unit_testing')

                if (environment == 'development' and debug is True) or \
                        (environment == 'testing' and unit_testing is True):
                    print_warning('Dropping all models...')
                    self.drop_all()

            if config_services.get_active('database', 'create_on_startup') is True:
                print_info('Creating all models...')
                self.create_all()

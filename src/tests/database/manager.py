# -*- coding: utf-8 -*-
"""
database manager module.
"""

from pyrin.database.manager import DatabaseManager as BaseDatabaseManager


class DatabaseManager(BaseDatabaseManager):
    """
    database manager class.
    """

    def __init__(self):
        """
        initializes an instance of DatabaseManager.
        """

        BaseDatabaseManager.__init__(self)

    def get_binds(self):
        """
        gets a shallow copy of binds dictionary.

        :returns: dict(type entity: str bind_name)
        :rtype: dict
        """

        return self._binds.copy()

    def get_entity_to_engine_map(self):
        """
        gets a shallow copy of entity to engine map dictionary.

        :returns: dict(type entity: Engine engine)
        :rtype: dict
        """

        return self._entity_to_engine_map.copy()

    def get_engine_to_table_map(self):
        """
        gets a shallow copy of engine to table map dictionary.

        :returns: dict(Engine engine: list[Table] tables)
        :rtype: dict
        """

        return self._engine_to_table_map.copy()

    def get_all_engines(self):
        """
        gets all database engines.

        :returns: list[Engine]
        :rtype: list
        """

        engines = [self._get_engine()]
        engines.extend([engine for engine in self._get_bounded_engines().values()])

        return engines

    def remove_bind(self, entity):
        """
        removes the given entity from binds dictionary.

        :param type entity: entity type to be removed.
        """

        self._binds.pop(entity)

# -*- coding: utf-8 -*-
"""
database manager module.
"""

from pyrin.database.manager import DatabaseManager


class TestDatabaseManager(DatabaseManager):
    """
    test database manager class.
    """

    def __init__(self):
        """
        initializes an instance of TestDatabaseManager.
        """

        DatabaseManager.__init__(self)

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

    def remove_bind(self, entity):
        """
        removes the given entity from binds dictionary.

        :param type entity: entity type to be removed.
        """

        self._binds.pop(entity)

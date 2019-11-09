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
        :rtype: dict(type: str)
        """

        return self.__binds.copy()

    def get_bounded_engines(self):
        """
        gets a shallow copy of bounded engines dictionary.

        :returns: dict(str bind_name: Engine engine)
        :rtype: dict(str: Engine)
        """

        return self.__bounded_engines.copy()

    def get_entity_to_engine_map(self):
        """
        gets a shallow copy of entity to engine map dictionary.

        :returns: dict(type entity: Engine engine)
        :rtype: dict(type: Engine)
        """

        return self.__entity_to_engine_map.copy()

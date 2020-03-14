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

        super().__init__()

    def get_binds(self):
        """
        gets a shallow copy of binds dictionary.

        :returns: dict[type entity: str bind_name]
        :rtype: dict
        """

        return self._binds.copy()

    def get_all_engines(self):
        """
        gets all database engines.

        :returns: list[Engine]
        :rtype: list
        """

        engines = [self.get_default_engine()]
        engines.extend([engine for engine in self.get_bounded_engines().values()])

        return engines

    def remove_bind(self, entity):
        """
        removes the given entity from binds dictionary.

        :param type entity: entity type to be removed.
        """

        self._binds.pop(entity)

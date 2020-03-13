# -*- coding: utf-8 -*-
"""
model manager module.
"""

from sqlalchemy.util._collections import AbstractKeyedTuple

from pyrin.core.context import Manager
from pyrin.database.model.base import CoreEntity


class ModelManager(Manager):
    """
    model manager class.
    """

    def is_base_entity(self, value):
        """
        gets a value indicating that input value is an instance of base entity type.

        base entity type by default is `CoreEntity`.
        this method could be used where direct reference to base entity
        type produces an error on server startup.

        :param object value: value to be checked.

        :rtype: bool
        """

        return isinstance(value, self.get_base_entity_type())

    def is_base_keyed_tuple(self, value):
        """
        gets a value indicating that input value is an instance of base keyed tuple type.

        base keyed tuple type by default is `AbstractKeyedTuple`.
        `AbstractKeyedTuple` objects are those objects that are returned by sqlalchemy
        `Query` with columns or multiple entities.

        :param object value: value to be checked.

        :rtype: bool
        """

        return isinstance(value, self.get_base_keyed_tuple_type())

    def get_base_entity_type(self):
        """
        gets the application's base entity type.

        base entity type by default is `CoreEntity`.
        this method could be used where direct reference to base entity
        type produces an error on server startup.

        :rtype: type
        """

        return CoreEntity

    def get_base_keyed_tuple_type(self):
        """
        gets the application's base keyed tuple type.

        base keyed tuple type by default is `AbstractKeyedTuple`.
        `AbstractKeyedTuple` objects are those objects that are returned by sqlalchemy
        `Query` with columns or multiple entities.

        :rtype: type
        """

        return AbstractKeyedTuple

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

    def is_core_entity(self, value):
        """
        gets a value indicating that input value is an instance of `CoreEntity`.
        this method could be used where direct reference to `CoreEntity`
        produces an error.

        :param object value: value to be checked.

        :rtype: bool
        """

        return isinstance(value, CoreEntity)

    def is_abstract_keyed_tuple(self, value):
        """
        gets a value indicating that input value is an instance
        of `AbstractKeyedTuple`. `AbstractKeyedTuple` objects are
        those objects that are returned by sqlalchemy `Query`
        with columns or multiple entities.

        :param object value: value to be checked.

        :rtype: bool
        """

        return isinstance(value, AbstractKeyedTuple)

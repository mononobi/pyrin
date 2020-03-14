# -*- coding: utf-8 -*-
"""
serializer keyed_tuple module.
"""

from sqlalchemy.util._collections import AbstractKeyedTuple

from pyrin.converters.serializer.decorators import serializer
from pyrin.converters.serializer.handlers.base import SerializerBase
from pyrin.utils.sqlalchemy import keyed_tuple_to_dict


@serializer()
class CoreKeyedTupleSerializer(SerializerBase):
    """
    core keyed tuple serializer class.
    """

    def _serialize(self, value, **options):
        """
        serializes the given value.

        :param AbstractKeyedTuple value: abstract keyed tuple value to be serialized.

        :keyword list[str] columns: the column names to be included in result.
                                    if not provided, all columns will be returned.
                                    note that the columns must be a subset of all
                                    columns of this `AbstractKeyedTuple`, otherwise
                                    it raises an error.

        :raises ColumnNotExistedError: column not existed error.

        :type: dict
        """

        return keyed_tuple_to_dict(value, **options)

    @property
    def accepted_type(self):
        """
        gets the accepted type for this serializer.

        which could serialize values from this type.

        :rtype: AbstractKeyedTuple
        """

        return AbstractKeyedTuple

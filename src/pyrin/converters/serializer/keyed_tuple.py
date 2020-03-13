# -*- coding: utf-8 -*-
"""
serializer keyed_tuple module.
"""

from pyrin.converters.serializer.base import SerializerBase
from pyrin.utils.sqlalchemy import keyed_tuple_to_dict


class CoreKeyedTupleSerializer(SerializerBase):
    """
    core keyed tuple serializer class.
    """

    def serialize(self, value, **options):
        """
        serializes the given value.

        :param AbstractKeyedTuple value: keyed tuple value to be serialized.

        :keyword list[str] columns: the column names to be included in result.
                                    if not provided, all columns will be returned.
                                    note that the columns must be a subset of all
                                    columns of this `AbstractKeyedTuple`, otherwise
                                    it raises an error.

        :raises ColumnNotExistedError: column not existed error.

        :rtype: dict
        """

        return keyed_tuple_to_dict(value, **options)

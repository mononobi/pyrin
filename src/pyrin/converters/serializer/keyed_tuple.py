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

    @classmethod
    def serialize(cls, value, **options):
        """
        serializes the given value.

        :param AbstractKeyedTuple value: keyed tuple value to be serialized.

        :rtype: dict
        """

        return keyed_tuple_to_dict(value)

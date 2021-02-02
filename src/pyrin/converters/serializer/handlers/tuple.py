# -*- coding: utf-8 -*-
"""
serializer handlers tuple module.
"""

import pyrin.converters.serializer.services as serializer_services

from pyrin.converters.serializer.decorators import serializer
from pyrin.converters.serializer.handlers.base import SerializerBase
from pyrin.core.globals import ROW_RESULT


@serializer()
class TupleSerializer(SerializerBase):
    """
    tuple serializer class.
    """

    def _serialize(self, value, **options):
        """
        serializes the given value.

        returns serialized tuple on success or `NULL` object if serialization fails.

        :param tuple[object] value: tuple value to be serialized.

        :keyword ResultSchema result_schema: result schema instance to be
                                             used to create computed columns.
                                             defaults to None if not provided.

        :returns: serialized tuple of objects
        :rtype: tuple[dict]
        """

        if len(value) <= 0:
            return ()

        result = []
        for item in value:
            result.append(serializer_services.serialize(item, **options))

        return tuple(result)

    @property
    def accepted_type(self):
        """
        gets the accepted type for this serializer.

        which could serialize values from this type.

        :rtype: type[tuple]
        """

        return tuple

    def is_serializable(self, value, **options):
        """
        gets a value indicating that the given input is serializable.

        :param object value: value to be serialized.

        :rtype: bool
        """

        return super().is_serializable(value, **options) and not isinstance(value, ROW_RESULT)

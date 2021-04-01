# -*- coding: utf-8 -*-
"""
serializer handlers tuple module.
"""

import pyrin.converters.serializer.services as serializer_services

from pyrin.converters.serializer.decorators import serializer
from pyrin.converters.serializer.handlers.base import SerializerBase


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

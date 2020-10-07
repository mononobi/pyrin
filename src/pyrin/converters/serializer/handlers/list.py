# -*- coding: utf-8 -*-
"""
serializer handlers list module.
"""

import pyrin.converters.serializer.services as serializer_services

from pyrin.converters.serializer.decorators import serializer
from pyrin.converters.serializer.handlers.base import SerializerBase


@serializer()
class ListSerializer(SerializerBase):
    """
    list serializer class.
    """

    def _serialize(self, value, **options):
        """
        serializes the given value.

        returns serialized list on success or `NULL` object if serialization fails.

        :param list[object] value: list value to be serialized.

        :returns: serialized list of objects
        :rtype: list[dict]
        """

        if len(value) <= 0:
            return []

        result = []
        for item in value:
            result.append(serializer_services.serialize(item, **options))

        return result

    @property
    def accepted_type(self):
        """
        gets the accepted type for this serializer.

        which could serialize values from this type.

        :rtype: type[list]
        """

        return list

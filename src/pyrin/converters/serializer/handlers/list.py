# -*- coding: utf-8 -*-
"""
serializer list module.
"""

import pyrin.converters.serializer.services as serializer_services

from pyrin.converters.serializer.decorators import serializer
from pyrin.converters.serializer.handlers.base import SerializerBase
from pyrin.core.globals import NULL


# @serializer()
class SimpleListSerializer(SerializerBase):
    """
    simple list serializer class.

    note that this serializer assumes all items types are same
    as the first item type. it is implemented this way to impact
    on performance as low as possible.
    if you want a list serializer to support items of different
    types, you could implement a new list serializer handler and
    register it to replace this.
    """

    def _serialize(self, value, **options):
        """
        serializes the given value.

        returns serialized value on success or `NULL` object if serialization fails.

        :param list[object] value: list value to be serialized.

        :rtype: list[dict]
        """

        if len(value) <= 0:
            return []

        first_item = value[0]
        converter = serializer_services.get_serializer(type(first_item))
        if converter is None:
            return NULL

        result = []
        for item in value:
            converted_item = converter.serialize(item, **options)
            if converted_item is NULL:
                result.append(item)
            else:
                result.append(converted_item)

        return result

    @property
    def accepted_type(self):
        """
        gets the accepted type for this serializer.

        which could serialize values from this type.

        :rtype: BaseEntity
        """

        return list


@serializer()
class ListSerializer(SerializerBase):
    """
    list serializer class.
    """

    def _serialize(self, value, **options):
        """
        serializes the given value.

        :param list[object] value: list value to be serialized.

        :returns: serialized list of objects
        :rtype: list
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

        :rtype: list
        """

        return list

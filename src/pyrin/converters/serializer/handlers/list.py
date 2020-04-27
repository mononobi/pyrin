# -*- coding: utf-8 -*-
"""
serializer handlers list module.
"""

import pyrin.converters.serializer.services as serializer_services

from pyrin.converters.serializer.decorators import serializer
from pyrin.converters.serializer.handlers.base import SerializerBase
from pyrin.core.globals import NULL


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

        :keyword bool check_first_item: specifies that if the first item in the given
                                        list is not serializable, don't try to serialize
                                        other items and return `NULL` object instead.
                                        this argument is provided to help preventing
                                        performance reduction on list serialization
                                        when list contains not serializable items.
                                        defaults to True if not provided.

        :returns: serialized list of objects
        :rtype: list[dict]
        """

        if len(value) <= 0:
            return []

        check_first_item = options.get('check_first_item', True)
        if check_first_item is not False:
            first = value[0]
            serialized_first = serializer_services.serialize(first, **options)
            if first is serialized_first:
                return NULL

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

# -*- coding: utf-8 -*-
"""
serializer handlers tuple module.
"""

import pyrin.converters.serializer.services as serializer_services

from pyrin.converters.serializer.decorators import serializer
from pyrin.converters.serializer.handlers.base import SerializerBase
from pyrin.core.globals import NULL, ROW_RESULT


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

        :keyword bool check_first_item: specifies that if the first item in the given
                                        tuple is not serializable, don't try to serialize
                                        other items and return `NULL` object instead.
                                        this argument is provided to help preventing
                                        performance reduction on tuple serialization
                                        when tuple contains not serializable items.
                                        defaults to True if not provided.

        :returns: serialized tuple of objects
        :rtype: tuple[dict]
        """

        if len(value) <= 0:
            return ()

        check_first_item = options.get('check_first_item', True)
        if check_first_item is not False:
            first = value[0]
            serialized_first = serializer_services.serialize(first, **options)
            if first is serialized_first:
                return NULL

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
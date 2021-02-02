# -*- coding: utf-8 -*-
"""
serializer handlers dictionary module.
"""

import pyrin.converters.serializer.services as serializer_services

from pyrin.core.structs import DTO
from pyrin.converters.serializer.decorators import serializer
from pyrin.converters.serializer.handlers.base import SerializerBase


@serializer()
class DictionarySerializer(SerializerBase):
    """
    dictionary serializer class.
    """

    def _serialize(self, value, **options):
        """
        serializes the given value.

        :param dict value: dict value to be serialized.

        :keyword ResultSchema result_schema: result schema instance to be
                                             used to create computed columns.
                                             defaults to None if not provided.

        :rtype: dict
        """

        result = DTO(value)
        for key, item in result.items():
            result[key] = serializer_services.serialize(item, **options)

        return result

    @property
    def accepted_type(self):
        """
        gets the accepted type for this serializer.

        which could serialize values from this type.

        :rtype: type[dict]
        """

        return dict

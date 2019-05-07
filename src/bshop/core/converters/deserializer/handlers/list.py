# -*- coding: utf-8 -*-
"""
deserializer list module.
"""

import bshop.core.converters.deserializer.services as deserializer_services

from bshop.core.converters.deserializer.handlers.base import DeserializerBase
from bshop.core.converters.deserializer.decorators import deserializer


@deserializer()
class ListDeserializer(DeserializerBase):
    """
    list deserializer.
    """

    def __init__(self, **options):
        """
        creates an instance of ListDeserializer.
        """

        DeserializerBase.__init__(self, **options)

    def deserialize(self, value, **options):
        """
        deserializes every possible value available in input list.
        and gets a new deserialized list, leaving the input unchanged.

        :param list value: value that should be deserialized.

        :rtype: list
        """

        if not self.is_deserializable(value, **options):
            return None

        result = [item for item in value]

        index = 0
        for item in result:
            deserialized_value = None

            if self.is_deserializable(item, **options):
                deserialized_value = self.deserialize(item)
            else:
                deserialized_value = deserializer_services.deserialize(item)

            if deserialized_value is not None:
                result[index] = deserialized_value

            index += 1
            continue

        return result

    def get_accepted_type(self):
        """
        gets the accepted type for this deserializer
        which could deserialize values from this type.

        :rtype: type
        """

        return list

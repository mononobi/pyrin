# -*- coding: utf-8 -*-
"""
List deserializers module.
"""

import bshop.core.api.deserializers.services as deserializer_services

from bshop.core.api.deserializers.handlers.base import DeserializerBase
from bshop.core.api.deserializers.decorators import register


@register()
class ListDeserializer(DeserializerBase):
    """
    List deserializer.
    """

    def __init__(self, **options):
        """
        Creates an instance of ListDeserializer.
        """

        DeserializerBase.__init__(self, **options)

    def deserialize(self, value, **options):
        """
        Deserializes every possible value available in input list.
        And gets a new deserialized list, leaving the input unchanged.

        :param list value: value that should be deserialized.

        :rtype: list
        """

        if not self.is_deserializable(value, **options):
            return None

        result = [item for item in value]

        index = 0
        for item in result:
            deserialized_value = None

            if type(item) is self.accepted_type():
                deserialized_value = self.deserialize(item)
            else:
                deserialized_value = deserializer_services.deserialize(item)

            if deserialized_value is not None:
                result[index] = deserialized_value

            index += 1
            continue

        return result

    def accepted_type(self):
        """
        Gets the accepted type for this deserializer
        which could deserialize values from this type.

        :rtype: type
        """

        return list

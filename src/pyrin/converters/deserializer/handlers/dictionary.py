# -*- coding: utf-8 -*-
"""
deserializer dictionary module.
"""

import pyrin.converters.deserializer.services as deserializer_services

from pyrin.converters.deserializer.handlers.base import DeserializerBase
from pyrin.converters.deserializer.decorators import deserializer
from pyrin.core.context import DTO


@deserializer()
class DictionaryDeserializer(DeserializerBase):
    """
    dictionary deserializer class.
    """

    def __init__(self, **options):
        """
        creates an instance of DictionaryDeserializer.
        """

        DeserializerBase.__init__(self, **options)

    def deserialize(self, value, **options):
        """
        deserializes every possible value available in input dictionary.
        and gets a new deserialized dictionary, leaving the input unchanged.

        :param dict value: value that should be deserialized.

        :rtype: dict
        """

        if not self.is_deserializable(value, **options):
            return self.DESERIALIZATION_FAILED

        result = DTO(**value)

        for key in result.keys():
            item = result.get(key)
            deserialized_value = self.DESERIALIZATION_FAILED

            if self.is_deserializable(item, **options):
                deserialized_value = self.deserialize(item)
            else:
                deserialized_value = deserializer_services.deserialize(item)

            if deserialized_value is not self.DESERIALIZATION_FAILED:
                result[key] = deserialized_value
            continue

        return result

    def get_accepted_type(self):
        """
        gets the accepted type for this deserializer
        which could deserialize values from this type.

        :rtype: type
        """

        return dict

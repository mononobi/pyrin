# -*- coding: utf-8 -*-
"""
deserializer dictionary module.
"""

import bshop.core.api.deserializer.services as deserializer_services

from bshop.core.api.deserializer.handlers.base import DeserializerBase
from bshop.core.api.deserializer.decorators import register_deserializer
from bshop.core.context import DTO


@register_deserializer()
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
            return None

        result = DTO(**value)

        for key in result.keys():
            item = result.get(key)
            deserialized_value = None

            if self.is_deserializable(item, **options):
                deserialized_value = self.deserialize(item)
            else:
                deserialized_value = deserializer_services.deserialize(item)

            if deserialized_value is not None:
                result[key] = deserialized_value
            continue

        return result

    def accepted_type(self):
        """
        gets the accepted type for this deserializer
        which could deserialize values from this type.

        :rtype: type
        """

        return dict

# -*- coding: utf-8 -*-
"""
Dictionary deserializers module.
"""

import bshop.core.api.deserializers.services as deserializer_services

from bshop.core.api.deserializers.handlers.base import DeserializerBase
from bshop.core.api.deserializers.decorators import register
from bshop.core.context import DynamicObject


@register()
class DictionaryDeserializer(DeserializerBase):
    """
    Dictionary deserializer.
    """

    def __init__(self, **options):
        """
        Creates an instance of DictionaryDeserializer.
        """

        DeserializerBase.__init__(self, **options)

    def deserialize(self, value, **options):
        """
        Deserializes every possible value available in input dictionary.
        And gets a new deserialized dictionary, leaving the input unchanged.

        :param dict value: value that should be deserialized.

        :rtype: dict
        """

        if not self.is_deserializable(value, **options):
            return None

        result = DynamicObject(**value)

        for key in result.keys():
            value = result.get(key)
            deserialized_value = None

            if type(value) is self.accepted_type():
                deserialized_value = self.deserialize(value)
            else:
                deserialized_value = deserializer_services.deserialize(value)

            if deserialized_value is not None:
                result[key] = deserialized_value
            continue

        return result

    def accepted_type(self):
        """
        Gets the accepted type for this deserializer
        which could deserialize values from this type.

        :rtype: type
        """

        return dict

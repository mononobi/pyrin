# -*- coding: utf-8 -*-
"""
Deserializers manager module.
"""

from bshop.core.context import Component
from bshop.core.api.deserializers import get_deserializers


class DeserializersManager(Component):
    """
    Deserializers manager class.
    """

    def deserialize(self, value, **options):
        """
        Deserializes the given value.
        Returns None if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: object
        """

        deserialized_value = None
        for deserializer in get_deserializers():
            deserialized_value = deserializer.deserialize(value, **options)

            if deserialized_value is not None:
                return deserialized_value

            continue

        return deserialized_value

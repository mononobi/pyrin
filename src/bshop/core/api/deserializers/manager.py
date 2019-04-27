# -*- coding: utf-8 -*-
"""
Deserializers manager module.
"""

from bshop.core.api.deserializers import _get_deserializers, _register_deserializer
from bshop.core.api.deserializers.handlers.base import DeserializerBase
from bshop.core.context import ObjectBase


class DeserializersManager(ObjectBase):
    """
    Deserializers manager class.
    """

    def deserialize(self, value, **options):
        """
        Deserializes the given value.
        Returns None if deserialization fails.

        :param object value: value to be deserialized.

        :rtype: object
        """

        options.update(accepted_type=type(value))
        deserialized_value = None

        for deserializer in self.get_deserializers(**options):
            deserialized_value = deserializer.deserialize(value, **options)

            if deserialized_value is not None:
                return deserialized_value
            continue

        return deserialized_value

    def register_deserializer(self, instance, **options):
        """
        Registers a new deserializer or updates the existing one if available.

        :param DeserializerBase instance: deserializer to be registered.
                                          it must be an instance of DeserializerBase.
        """

        _register_deserializer(instance, **options)

    def get_deserializers(self, **options):
        """
        Gets all registered deserializers.
        It could filter deserializers for a specific type if provided.

        :keyword type accepted_type: specifies to get deserializers which are registered for the
                                     accepted type. If not provided, all deserializers
                                     will be returned.

        :returns: list[instance]

        :rtype: list[DeserializerBase]
        """

        return _get_deserializers(**options)

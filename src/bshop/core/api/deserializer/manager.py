# -*- coding: utf-8 -*-
"""
deserializer manager module.
"""

from bshop.core.api.deserializer import _get_deserializers, _register_deserializer
from bshop.core.api.deserializer.handlers.base import DeserializerBase
from bshop.core.context import CoreObject


class DeserializerManager(CoreObject):
    """
    deserializer manager class.
    """

    def deserialize(self, value, **options):
        """
        deserializes the given value.
        returns None if deserialization fails.

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
        registers a new deserializer or replaces the existing one
        if `replace=True` is provided. otherwise, it raises an error
        on adding an instance which it's name and accepted type is already available
        in registered deserializers.

        :param DeserializerBase instance: deserializer to be registered.
                                          it must be an instance of DeserializerBase.

        :keyword bool replace: specifies that if there is another registered
                               deserializer with the same name and accepted type,
                               replace it with the new one, otherwise raise
                               an error. defaults to False.
        """

        _register_deserializer(instance, **options)

    def get_deserializers(self, **options):
        """
        gets all registered deserializers.
        it could filter deserializers for a specific type if provided.

        :keyword type accepted_type: specifies to get deserializers which are registered for the
                                     accepted type. if not provided, all deserializers
                                     will be returned.

        :rtype: list[DeserializerBase]
        """

        return _get_deserializers(**options)

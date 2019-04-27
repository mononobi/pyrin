# -*- coding: utf-8 -*-
"""
Deserializers services module.
"""

from bshop.core.api.deserializers.component import DeserializersComponent
from bshop.core.application.services import get_component


def deserialize(value, **options):
    """
    Deserializes the given value.
    Returns None if deserialization fails.

    :param object value: value to be deserialized.

    :rtype: object
    """

    return get_component(DeserializersComponent.COMPONENT_ID).deserialize(value, **options)


def register_deserializer(instance, **options):
    """
    Registers a new deserializer or updates the existing one if available.

    :param DeserializerBase instance: deserializer to be registered.
                                      it must be an instance of DeserializerBase.
    """

    return get_component(DeserializersComponent.COMPONENT_ID).register_deserializer(
        instance, **options)


def get_deserializers(**options):
    """
    Gets all registered deserializers.
    It could filter deserializers for a specific type if provided.

    :keyword type accepted_type: specifies to get deserializers which are registered for the
                                 accepted type. If not provided, all deserializers
                                 will be returned.

    :returns: list[instance]

    :rtype: list[DeserializerBase]
    """

    return get_component(DeserializersComponent.COMPONENT_ID).get_deserializers(**options)

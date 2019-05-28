# -*- coding: utf-8 -*-
"""
deserializer services module.
"""

from pyrin.converters.deserializer import DeserializerPackage
from pyrin.application.services import get_component


def deserialize(value, **options):
    """
    deserializes the given value.
    returns `DESERIALIZATION_FAILED` object if deserialization fails.

    :param object value: value to be deserialized.

    :rtype: object
    """

    return get_component(DeserializerPackage.COMPONENT_NAME, **options).\
        deserialize(value, **options)


def register_deserializer(instance, **options):
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

    :raises InvalidDeserializerTypeError: invalid deserializer type error.
    :raises DuplicatedDeserializerError: duplicated deserializer error.
    """

    return get_component(DeserializerPackage.COMPONENT_NAME, **options).\
        register_deserializer(instance, **options)


def get_deserializers(**options):
    """
    gets all registered deserializers.
    it could filter deserializer for a specific type if provided.

    :keyword type accepted_type: specifies to get deserializers which are registered for the
                                 accepted type. if not provided, all deserializers
                                 will be returned.

    :rtype: list[DeserializerBase]
    """

    return get_component(DeserializerPackage.COMPONENT_NAME, **options).\
        get_deserializers(**options)

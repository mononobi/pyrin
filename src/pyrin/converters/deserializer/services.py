# -*- coding: utf-8 -*-
"""
deserializer services module.
"""

from pyrin.converters.deserializer import DeserializerPackage
from pyrin.application.services import get_component


def deserialize(value, **options):
    """
    deserializes the given value.

    returns deserialized object on success or returns
    the same input value if deserialization fails.

    :param object value: value to be deserialized.

    :keyword bool include_internal: specifies that any chained internal deserializer
                                    must also be used for deserialization. if set to
                                    False, only non-internal deserializers will be used.
                                    defaults to True if not provided.

    :returns: deserialized object
    """

    return get_component(DeserializerPackage.COMPONENT_NAME).deserialize(value, **options)


def register_deserializer(instance, **options):
    """
    registers a new deserializer or replaces the existing one.

    if `replace=True` is provided. otherwise, it raises an error
    on adding a deserializer which is already registered.

    :param AbstractDeserializerBase instance: deserializer to be registered.
                                              it must be an instance of
                                              AbstractDeserializerBase.

    :keyword bool replace: specifies that if there is another registered
                           deserializer with the same name and accepted type,
                           replace it with the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidDeserializerTypeError: invalid deserializer type error.
    :raises DuplicatedDeserializerError: duplicated deserializer error.
    """

    return get_component(DeserializerPackage.COMPONENT_NAME).register_deserializer(instance,
                                                                                   **options)


def get_deserializers(**options):
    """
    gets all registered deserializers.

    it could filter deserializers for a specific type if provided.
    it only returns the first deserializer for each type, because
    all deserializers for a given type, are chained together.

    :keyword type accepted_type: specifies to get deserializers which are registered for
                                 the accepted type. if not provided, all deserializers
                                 will be returned.

    :rtype: list[AbstractDeserializerBase]
    """

    return get_component(DeserializerPackage.COMPONENT_NAME).get_deserializers(**options)

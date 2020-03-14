# -*- coding: utf-8 -*-
"""
serializer services module.
"""

from pyrin.converters.serializer import SerializerPackage
from pyrin.application.services import get_component


def serialize(value, **options):
    """
    serializes the given value.

    returns serialized dict or list of dicts on success
    or returns the same input value if serialization fails.

    all extra keyword arguments will be passed to underlying serializer.

    :param object | list[object] value: value or values to be serialized.

    :rtype: dict | list[dict]
    """

    return get_component(SerializerPackage.COMPONENT_NAME).serialize(value, **options)


def register_serializer(instance, **options):
    """
    registers a new serializer or replaces the existing one.

    if `replace=True` is provided. otherwise, it raises an error
    on adding a serializer which is already registered.

    :param AbstractSerializerBase instance: serializer to be registered.
                                            it must be an instance of
                                            AbstractSerializerBase.

    :keyword bool replace: specifies that if there is another registered
                           serializer with the same accepted type,
                           replace it with the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidSerializerTypeError: invalid serializer type error.
    :raises DuplicatedSerializerError: duplicated serializer error.
    """

    return get_component(SerializerPackage.COMPONENT_NAME).register_serializer(instance,
                                                                               **options)


def get_serializer(accepted_type):
    """
    gets the registered serializer for given type.

    it returns None if no serializer found for given type.

    :param type accepted_type: gets the serializer which is
                               registered for the accepted type.

    :rtype: AbstractSerializerBase
    """

    return get_component(SerializerPackage.COMPONENT_NAME).get_serializer(accepted_type)

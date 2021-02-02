# -*- coding: utf-8 -*-
"""
serializer services module.
"""

from pyrin.converters.serializer import SerializerPackage
from pyrin.application.services import get_component


def serialize(value, **options):
    """
    serializes the given value.

    returns serialized value on success or the
    same input value if serialization fails.

    all extra keyword arguments will be passed to underlying serializer.

    :param object value: value to be serialized.

    :keyword ResultSchema result_schema: result schema instance to be
                                         used to create computed columns.
                                         defaults to None if not provided.

    :returns: serialized object
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


def get_serializers(accepted_type):
    """
    gets the registered serializers for given type.

    it returns an empty list if no serializer found for given type.

    :param type accepted_type: gets the serializers which are
                               registered for the accepted type.

    :rtype: list[AbstractSerializerBase]
    """

    return get_component(SerializerPackage.COMPONENT_NAME).get_serializers(accepted_type)

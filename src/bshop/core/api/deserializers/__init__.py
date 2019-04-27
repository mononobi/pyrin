# -*- coding: utf-8 -*-
"""
API deserializers package.
"""

from bshop.core.api.deserializers.handlers.base import DeserializerBase
from bshop.core.context import Context
from bshop.core.exceptions import CoreTypeError

__deserializers__ = Context()


def _register_deserializer(instance, **options):
    """
    Registers a new deserializer or updates the existing one if available.

    :param DeserializerBase instance: deserializer to be registered.
                                      it must be an instance of DeserializerBase.

    :raises CoreTypeError: core type error.
    """

    if not isinstance(instance, DeserializerBase):
        raise CoreTypeError('Input parameter [{instance}] is '
                            'not an instance of DeserializerBase.'
                            .format(instance=str(instance)))

    global __deserializers__
    __deserializers__[(instance.get_name(), instance.accepted_type())] = instance


def _get_deserializers(**options):
    """
    Gets all registered deserializers.
    It could filter deserializers for a specific type if provided.

    :keyword type accepted_type: specifies to get deserializers which are registered for the
                                 accepted type. If not provided, all deserializers will be returned.

    :returns: list[instance]

    :rtype: list[DeserializerBase]
    """

    accepted_type = options.get('accepted_type', None)

    if accepted_type is None:
        return [value for value in __deserializers__.values()]

    # getting all deserializers that are registered for the given type.
    deserializer_keys = [key for key in __deserializers__.keys() if key[1] == accepted_type]
    return [__deserializers__[key] for key in deserializer_keys]

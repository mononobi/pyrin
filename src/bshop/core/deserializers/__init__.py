# -*- coding: utf-8 -*-
"""
Deserializers package.
"""

from bshop.core.deserializers.base import DeserializerBase
from bshop.core.deserializers.datetime import DateTimeDeserializer

__deserializers__ = {}


def register_deserializer(instance):
    """
    Registers a new deserializer or updates the existing one if available.

    :param DeserializerBase instance: deserializer to be registered.
                                      it must be an instance of DeserializerBase.

    """

    if not isinstance(instance, DeserializerBase):
        raise TypeError('input parameter [{instance_name}] is'
                        'not an instance of DeserializerBase.'
                        .format(instance_name=instance.get_name()))

    global __deserializers__
    __deserializers__[instance.get_name()] = instance


def get_deserializers():
    """
    Gets all registered deserializers.

    :rtype: list[DeserializerBase]
    """

    return __deserializers__

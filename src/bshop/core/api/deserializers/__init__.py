# -*- coding: utf-8 -*-
"""
API deserializers package.
"""

from bshop.core.api.deserializers.base import DeserializerBase
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
    __deserializers__[instance.get_name()] = instance


def get_deserializers(**options):
    """
    Gets all registered deserializers.

    :returns: dict{str, DeserializerBase}

    :rtype: dict
    """

    return __deserializers__

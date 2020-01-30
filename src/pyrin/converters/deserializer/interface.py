# -*- coding: utf-8 -*-
"""
deserializer interface module.
"""

from threading import Lock

from pyrin.core.context import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.utils.singleton import MultiSingletonMeta


class DeserializerSingletonMeta(MultiSingletonMeta):
    """
    deserializer singleton meta class.
    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class AbstractDeserializerBase(CoreObject, metaclass=DeserializerSingletonMeta):
    """
    abstract deserializer base class.
    """

    def deserialize(self, value, **options):
        """
        deserializes the given value.
        returns `NULL` object if deserialization fails.

        :param object value: value to be deserialized.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: deserialized value.
        """

        raise CoreNotImplementedError()

    def set_next(self, deserializer):
        """
        sets the next deserializer handler and returns it.

        :param Union[AbstractDeserializerBase, None] deserializer: deserializer instance to
                                                                   be set as next handler.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: AbstractDeserializerBase
        """

        raise CoreNotImplementedError()

    def get_accepted_type(self):
        """
        gets the accepted type for this deserializer
        which could deserialize values from this type.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: type
        """

        raise CoreNotImplementedError()

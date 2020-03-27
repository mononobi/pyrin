# -*- coding: utf-8 -*-
"""
deserializer interface module.
"""

from abc import abstractmethod
from threading import Lock

from pyrin.core.structs import CoreObject, MultiSingletonMeta
from pyrin.core.exceptions import CoreNotImplementedError


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

    @abstractmethod
    def deserialize(self, value, **options):
        """
        deserializes the given value.

        returns `NULL` object if deserialization fails.

        :param object value: value to be deserialized.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: deserialized value.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def set_next(self, deserializer):
        """
        sets the next deserializer handler and returns it.

        :param AbstractDeserializerBase deserializer: deserializer instance to
                                                      be set as next handler.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: AbstractDeserializerBase
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def accepted_type(self):
        """
        gets the accepted type for this deserializer.

        which could deserialize values from this type.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: type
        """

        raise CoreNotImplementedError()

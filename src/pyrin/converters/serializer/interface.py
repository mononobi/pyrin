# -*- coding: utf-8 -*-
"""
serializer interface module.
"""

from abc import abstractmethod
from threading import Lock

from pyrin.core.structs import CoreObject, MultiSingletonMeta
from pyrin.core.exceptions import CoreNotImplementedError


class SerializerSingletonMeta(MultiSingletonMeta):
    """
    serializer singleton meta class.

    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class AbstractSerializerBase(CoreObject, metaclass=SerializerSingletonMeta):
    """
    abstract serializer base class.
    """

    @abstractmethod
    def serialize(self, value, **options):
        """
        serializes the given value.

        returns serialized dict or list of dicts on success
        or returns `NULL` object if serialization fails.

        :param object | list[object] value: value or values to be serialized.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: dict | list[dict]
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def accepted_type(self):
        """
        gets the accepted type for this serializer.

        which could serialize values from this type.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: type
        """

        raise CoreNotImplementedError()

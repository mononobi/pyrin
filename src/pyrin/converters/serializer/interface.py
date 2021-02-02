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

        returns serialized value on success or `NULL` object if serialization fails.

        :param object value: value to be serialized.

        :keyword ResultSchema result_schema: result schema instance to be
                                             used to create computed columns.
                                             defaults to None if not provided.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: serialized object
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

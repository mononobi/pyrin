# -*- coding: utf-8 -*-
"""
serializer handlers base module.
"""

from abc import abstractmethod

from pyrin.converters.serializer.interface import AbstractSerializerBase
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.core.globals import NULL


class SerializerBase(AbstractSerializerBase):
    """
    serializer base class.

    all application serializers must inherit from this.
    """

    def __init__(self, *args, **options):
        """
        initializes an instance of SerializerBase.

        :param object args: constructor arguments.
        """

        super().__init__()

    def serialize(self, value, **options):
        """
        serializes the given value.

        returns serialized value on success or `NULL` object if serialization fails.

        :param object value: value to be serialized.

        :keyword ResultSchema result_schema: result schema instance to be
                                             used to create computed columns.
                                             defaults to None if not provided.

        :returns: serialized object
        :rtype: dict | list[dict]
        """

        if self.is_serializable(value, **options) is False:
            return NULL

        return self._serialize(value, **options)

    @abstractmethod
    def _serialize(self, value, **options):
        """
        serializes the given value.

        this method must be implemented by subclasses.

        :param object value: value to be serialized.

        :keyword ResultSchema result_schema: result schema instance to be
                                             used to create computed columns.
                                             defaults to None if not provided.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: serialized object
        :rtype: dict | list[dict]
        """

        raise CoreNotImplementedError()

    def is_serializable(self, value, **options):
        """
        gets a value indicating that the given input is serializable.

        :param object value: value to be serialized.

        :rtype: bool
        """

        return isinstance(value, self.accepted_type)

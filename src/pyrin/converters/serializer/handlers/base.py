# -*- coding: utf-8 -*-
"""
serializer base module.
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

        returns serialized dict or list of dicts on success
        or returns `NULL` object if serialization fails.

        :param Union[object, list[object]] value: value or values to be serialized.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: Union[dict, list[dict]]
        """

        if isinstance(value, list):
            if len(value) > 0 and self.is_serializable(value[0]):
                return self._serialize_list(value, **options)

        elif self.is_serializable(value):
            return self._serialize(value, **options)

        return NULL

    def is_serializable(self, value, **options):
        """
        gets a value indicating that the given input is serializable.

        :param Union[object, list[object] value: value or values to be serialized.

        :rtype: bool
        """

        return isinstance(value, self.accepted_type)

    @abstractmethod
    def _serialize(self, value, **options):
        """
        serializes the given value.

        :param object value: value to be serialized.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: dict
        """

        raise CoreNotImplementedError()

    def _serialize_list(self, values, **options):
        """
        serializes the given values.

        :param list[object] values: values to be serialized.

        :rtype: list[dict]
        """

        if values is None or len(values) == 0:
            return []

        return [self._serialize(value, **options) for value in values]

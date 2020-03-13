# -*- coding: utf-8 -*-
"""
serializer base module.
"""

from abc import abstractmethod

from pyrin.core.context import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError


class SerializerBase(CoreObject):
    """
    serializer base class.

    all application serializers must inherit from this.
    """

    @abstractmethod
    def serialize(self, value, **options):
        """
        serializes the given value.

        :param object value: value to be serialized.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: dict
        """

        raise CoreNotImplementedError()

    def serialize_list(self, values, **options):
        """
        serializes the given list of values.

        :param list[object] values: values to be serialized.

        :returns: list[dict]
        :rtype: list
        """

        if values is None or len(values) == 0:
            return []

        return [self.serialize(value, **options) for value in values]

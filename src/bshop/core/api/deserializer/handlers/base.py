# -*- coding: utf-8 -*-
"""
deserializer base module.
"""

from bshop.core.context import CoreObject
from bshop.core.exceptions import CoreNotImplementedError


class DeserializerBase(CoreObject):
    """
    base deserializer class.
    """

    def __init__(self, **options):
        CoreObject.__init__(self)

    def deserialize(self, value, **options):
        """
        deserializes the given value.

        :param object value: value to be deserialized.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: deserialized value.
        """

        raise CoreNotImplementedError()

    def is_deserializable(self, value, **options):
        """
        gets a value indicating that the given input is deserializable.

        :param object value: value to be deserialized.

        :rtype: bool
        """

        return isinstance(value, self.accepted_type())

    def accepted_type(self):
        """
        gets the accepted type for this deserializer
        which could deserialize values from this type.

        :rtype: type
        """

        raise CoreNotImplementedError()


class StringDeserializerBase(DeserializerBase):
    """
    base string deserializer class.
    """

    def __init__(self, **options):
        DeserializerBase.__init__(self)

    def deserialize(self, value, **options):
        """
        deserializes the given value.

        :param str value: value to be deserialized.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: deserialized value.
        """

        raise CoreNotImplementedError()

    def is_deserializable(self, value, **options):
        """
        gets a value indicating that the given input is deserializable.

        :param object value: value to be deserialized.

        :rtype: bool
        """

        is_valid_type = DeserializerBase.is_deserializable(self, value, **options)

        if is_valid_type:
            if len(value.strip()) == 0:
                return False

        return is_valid_type

    def accepted_type(self):
        """
        gets the accepted type for this deserializer
        which could deserialize values from this type.

        :rtype: type
        """

        return str

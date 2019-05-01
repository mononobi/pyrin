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

        :rtype: object
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

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: type
        """

        raise CoreNotImplementedError()


class StringDeserializerBase(DeserializerBase):
    """
    base string deserializer class.
    """

    def __init__(self, **options):
        """
        initializes an instance of StringDeserializerBase.

        :keyword list[tuple(str, int)] accepted_formats: custom string formats that this
                                                         deserializer can deserialize value from.
        """

        DeserializerBase.__init__(self, **options)

        # setting default accepted formats.
        self._accepted_formats = self.get_default_formats()

        # setting custom accepted formats
        custom_accepted_formats = options.get('accepted_formats', [])
        self._accepted_formats.extend(custom_accepted_formats)

        # min and max accepted length of strings
        # to be deserialized by this deserializer.
        self._min_length, self._max_length = self._calculate_accepted_length()

    def deserialize(self, value, **options):
        """
        deserializes the given value.

        :param str value: value to be deserialized.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: deserialized value.

        :rtype: object
        """

        raise CoreNotImplementedError()

    def is_deserializable(self, value, **options):
        """
        gets a value indicating that the given input is deserializable.

        :param object value: value to be deserialized.

        :rtype: bool
        """

        if DeserializerBase.is_deserializable(self, value, **options) \
                and self.is_valid_length(value):
            return True

        return False

    def accepted_type(self):
        """
        gets the accepted type for this deserializer
        which could deserialize values from this type.

        :rtype: type
        """

        return str

    def accepted_length(self):
        """
        gets the min and max accepted length of strings to be
        deserialized by this deserializer.

        :returns tuple(int min, int max)

        :rtype: tuple(int, int)
        """

        return self._min_length, self._max_length

    def accepted_formats(self):
        """
        gets the accepted string formats that this deserializer
        can deserialize value from.

        :returns: list(tuple(str format, int length))

        :rtype: list(tuple(str, int))
        """

        return self._accepted_formats

    def is_valid_length(self, value):
        """
        gets a value indicating that input value has valid
        length to be deserialized by this deserializer.

        :param str value: value to be deserialized.

        :rtype: bool
        """

        length = len(value.strip())
        min_length, max_length = self.accepted_length()

        if length < min_length or length > max_length:
            return False

        return True

    def _calculate_accepted_length(self):
        """
        calculates the min and max accepted length of values
        to be deserialized by this deserializer.

        :returns: tuple(int min, int max)

        :rtype: tuple(int, int)
        """

        return min([item[1] for item in self.accepted_formats()]), \
            max([item[1] for item in self.accepted_formats()])

    @classmethod
    def get_default_formats(cls):
        """
        gets default accepted formats that this
        deserializer could deserialize value from.

        :raises CoreNotImplementedError: core not implemented error.

        :return: list(tuple(str format, int length))

        :rtype: list(tuple(str, int))
        """

        raise CoreNotImplementedError()


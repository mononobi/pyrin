# -*- coding: utf-8 -*-
"""
deserializer boolean module.
"""

from pyrin.converters.deserializer.handlers.base import StringDeserializerBase
from pyrin.converters.deserializer.decorators import deserializer


@deserializer()
class BooleanDeserializer(StringDeserializerBase):
    """
    boolean deserializer class.
    """

    def __init__(self, **options):
        """
        creates an instance of BooleanDeserializer.

        :keyword list[tuple(str, int)] accepted_formats: a list of custom accepted string
                                                         formats and their length for
                                                         boolean deserialization.

        :type accepted_formats: list[tuple(str format, int length)]
        """

        StringDeserializerBase.__init__(self, **options)

    def deserialize(self, value, **options):
        """
        deserializes the given value.
        returns None if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: bool
        """

        if not self.is_deserializable(value, **options):
            return None

        value = value.strip()
        converted_bool = None

        if value.lower() is 'true':
            converted_bool = True
        elif value.lower() is 'false':
            converted_bool = False

        return converted_bool

    @classmethod
    def get_default_formats(cls):
        """
        gets default accepted formats that this
        deserializer could deserialize value from.

        :return: list(tuple(str format, int length))

        :rtype: list(tuple(str, int))
        """

        return [('true', 4),
                ('false', 5)]

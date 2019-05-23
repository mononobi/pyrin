# -*- coding: utf-8 -*-
"""
deserializer boolean module.
"""

import re

from pyrin.converters.deserializer.handlers.base import StringPatternDeserializerBase
from pyrin.converters.deserializer.decorators import deserializer


@deserializer()
class BooleanDeserializer(StringPatternDeserializerBase):
    """
    boolean deserializer class.
    """

    # matches the bool inside string.
    # example: true, false
    # matching are case-insensitive.
    TRUE_REGEX = re.compile(r'^true$', re.IGNORECASE)
    FALSE_REGEX = re.compile(r'^false$', re.IGNORECASE)

    def __init__(self, **options):
        """
        creates an instance of BooleanDeserializer.

        :keyword list[tuple(Pattern, int)] accepted_formats: a list of custom accepted formats
                                                             and their length for boolean
                                                             deserialization.

        :type accepted_formats: list[tuple(Pattern format, int length)]
        """

        StringPatternDeserializerBase.__init__(self, **options)

        self._converter_map = {self.TRUE_REGEX: True,
                               self.FALSE_REGEX: False}

    def deserialize(self, value, **options):
        """
        deserializes the given value.
        returns None if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: bool
        """

        deserializable, pattern = self.is_deserializable(value, **options)
        if not deserializable:
            return None

        return self._converter_map[pattern]

    def get_default_formats(self):
        """
        gets default accepted formats that this
        deserializer could deserialize value from.

        :return: list(tuple(Pattern format, int length))

        :rtype: list(tuple(Pattern, int))
        """

        return [(self.TRUE_REGEX, 4),
                (self.FALSE_REGEX, 5)]

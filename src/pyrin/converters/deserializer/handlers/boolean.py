# -*- coding: utf-8 -*-
"""
deserializer boolean module.
"""

import re

from pyrin.converters.deserializer.handlers.base import StringPatternDeserializerBase
from pyrin.converters.deserializer.decorators import deserializer
from pyrin.core.globals import NULL


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

        super().__init__(**options)

        self._converter_map = self._get_converter_map()

    def _deserialize(self, value, **options):
        """
        deserializes the given value.
        returns `NULL` object if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: bool
        """

        deserializable, pattern = self.is_deserializable(value, **options)
        if not deserializable:
            return NULL

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

    def _get_converter_map(self):
        """
        gets converter map dictionary.

        :returns: dict(Pattern format: bool value)

        :rtype: dict
        """

        return {self.TRUE_REGEX: True,
                self.FALSE_REGEX: False}

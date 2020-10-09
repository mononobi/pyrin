# -*- coding: utf-8 -*-
"""
deserializer handlers boolean module.
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
    # matching is case-insensitive.
    TRUE_REGEX = re.compile(r'^true$', re.IGNORECASE)
    FALSE_REGEX = re.compile(r'^false$', re.IGNORECASE)

    def __init__(self, **options):
        """
        creates an instance of BooleanDeserializer.

        :keyword list[tuple[Pattern, int, int]] accepted_formats: a list of custom accepted
                                                                  formats and their min and
                                                                  max length for boolean
                                                                  deserialization.

        :note accepted_formats: list[tuple[Pattern format, int min_length, int max_length]]

        :keyword bool internal: specifies that this deserializer is internal.
                                internal deserializers will not be used for
                                deserializing client inputs.
                                defaults to False if not provided.
        """

        super().__init__(**options)

        self._converter_map = self._get_converter_map()

    def _deserialize(self, value, **options):
        """
        deserializes the given value.

        :param str value: value to be deserialized.

        :keyword Pattern matching_pattern: the pattern that has matched the value.

        :rtype: bool
        """

        pattern = options.pop('matching_pattern')
        return self._converter_map[pattern]

    @property
    def default_formats(self):
        """
        gets default accepted formats that this deserializer could deserialize value from.

        :returns: list[tuple[Pattern format, int min_length, int max_length]]
        :rtype: list[tuple[Pattern, int, int]]
        """

        return [(self.TRUE_REGEX, 4, 4),
                (self.FALSE_REGEX, 5, 5)]

    def _get_converter_map(self):
        """
        gets converter map dictionary.

        :returns: dict[Pattern format: bool value]
        :rtype: dict
        """

        return {self.TRUE_REGEX: True,
                self.FALSE_REGEX: False}

# -*- coding: utf-8 -*-
"""
deserializer handlers none module.
"""

import re

from pyrin.converters.deserializer.handlers.base import StringPatternDeserializerBase
from pyrin.converters.deserializer.decorators import deserializer


@deserializer()
class NoneDeserializer(StringPatternDeserializerBase):
    """
    none deserializer class.
    """

    # matches the none inside string.
    # example: none, null
    # matching is case-insensitive.
    NONE_REGEX = re.compile(r'^none$', re.IGNORECASE)
    NULL_REGEX = re.compile(r'^null$', re.IGNORECASE)

    def __init__(self, **options):
        """
        creates an instance of NoneDeserializer.

        :keyword list[tuple[Pattern, int, int]] accepted_formats: a list of custom accepted
                                                                  formats and their min and
                                                                  max length for None
                                                                  deserialization.

        :note accepted_formats: list[tuple[Pattern format, int min_length, int max_length]]

        :keyword bool internal: specifies that this deserializer is internal.
                                internal deserializers will not be used for
                                deserializing client inputs.
                                defaults to False if not provided.
        """

        super().__init__(**options)

    def _deserialize(self, value, **options):
        """
        deserializes the given value.

        :param str value: value to be deserialized.

        :keyword Pattern matching_pattern: the pattern that has matched the value.

        :rtype: None
        """

        return None

    @property
    def default_formats(self):
        """
        gets default accepted formats that this deserializer could deserialize value from.

        :returns: list[tuple[Pattern format, int min_length, int max_length]]
        :rtype: list[tuple[Pattern, int, int]]
        """

        return [(self.NONE_REGEX, 4, 4),
                (self.NULL_REGEX, 4, 4)]

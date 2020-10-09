# -*- coding: utf-8 -*-
"""
deserializer handlers string module.
"""

import re

from pyrin.converters.deserializer.decorators import deserializer
from pyrin.converters.deserializer.handlers.base import StringPatternDeserializerBase


@deserializer()
class StringDeserializer(StringPatternDeserializerBase):
    """
    string deserializer class.
    """

    # default min for this deserializer is 2 because it should
    # at least have two single or double quotes at both ends.
    DEFAULT_MIN = 2

    # matches a string value, all of these values will be matched.
    # example: "sample_value", "12345678", 'true'
    # note that the second and third examples will be deserialized as a
    # string with value 12345678 and true and won't deserialize as an
    # integer or boolean, because of the enclosing single or double quotes.
    DOUBLE_QUOTE_REGEX = re.compile(r'^[\"].*[\"]$')
    SINGLE_QUOTE_REGEX = re.compile(r'^[\'].*[\']$')

    def __init__(self, **options):
        """
        creates an instance of StringDeserializer.

        :keyword list[tuple[Pattern, int, int]] accepted_formats: a list of custom accepted
                                                                  patterns and their min and
                                                                  max length for string
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

        :rtype: str
        """

        # removing the first and last single or double quotes from value.
        value = value[1:-1]
        return value

    @property
    def default_formats(self):
        """
        gets default accepted patterns that this deserializer could deserialize value from.

        :returns: list[tuple[Pattern format, int min_length, int max_length]]
        :rtype: list[tuple[Pattern, int, int]]
        """

        return [(self.DOUBLE_QUOTE_REGEX, self.UNDEF_LENGTH, self.UNDEF_LENGTH),
                (self.SINGLE_QUOTE_REGEX, self.UNDEF_LENGTH, self.UNDEF_LENGTH)]

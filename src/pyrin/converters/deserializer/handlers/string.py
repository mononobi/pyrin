# -*- coding: utf-8 -*-
"""
deserializer string module.
"""

import re

from pyrin.converters.deserializer.decorators import deserializer
from pyrin.converters.deserializer.handlers.base import StringPatternDeserializerBase
from pyrin.core.globals import NULL


@deserializer()
class StringDeserializer(StringPatternDeserializerBase):
    """
    string deserializer class.
    """

    # default min for this deserializer is 2 because it should
    # at least has two single or double quotes at both ends.
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

        :keyword list[tuple(Pattern, int)] accepted_formats: a list of custom accepted patterns
                                                             and their length for string
                                                             deserialization.

        :type accepted_formats: list[tuple(Pattern format, int length)]
        """

        super().__init__(**options)

    def _deserialize(self, value, **options):
        """
        deserializes the given value.
        returns `NULL` object if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: str
        """

        deserializable, pattern = self.is_deserializable(value, **options)
        if not deserializable:
            return NULL

        # removing the first and last single or double quotes from value.
        value = value[1:-1]

        return value

    def get_default_formats(self):
        """
        gets default accepted patterns that this
        deserializer could deserialize value from.

        :return: list(tuple(Pattern format, int length))

        :rtype: list(tuple(Pattern, int))
        """

        return [(self.DOUBLE_QUOTE_REGEX, self.UNDEF_LENGTH),
                (self.SINGLE_QUOTE_REGEX, self.UNDEF_LENGTH)]

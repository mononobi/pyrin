# -*- coding: utf-8 -*-
"""
deserializer handlers number module.
"""

import re

from pyrin.converters.deserializer.handlers.base import StringPatternDeserializerBase
from pyrin.converters.deserializer.decorators import deserializer


@deserializer()
class IntegerDeserializer(StringPatternDeserializerBase):
    """
    integer deserializer class.
    """

    # matches the integer inside string.
    # example: 12, 232, 10, 0, -5, 70, -909
    # all of these values will be matched.
    # values that starting with '0' or '+' are not considered as integer.
    INTEGER_REGEX = re.compile(r'^(0|([-]?[1-9]([0-9])*))$')

    def __init__(self, **options):
        """
        creates an instance of IntegerDeserializer.

        :keyword list[tuple[Pattern, int, int]] accepted_formats: a list of custom accepted
                                                                  formats and their min and
                                                                  max length for integer
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

        :rtype: int
        """

        return int(value)

    @property
    def default_formats(self):
        """
        gets default accepted formats that this deserializer could deserialize value from.

        :returns: list[tuple[Pattern format, int min_length, int max_length]]
        :rtype: list[tuple[Pattern, int, int]]
        """

        return [(self.INTEGER_REGEX, self.UNDEF_LENGTH, self.UNDEF_LENGTH)]


@deserializer()
class FloatDeserializer(StringPatternDeserializerBase):
    """
    float deserializer class.
    """

    # default min for this deserializer is 3 because it
    # should at least have two digits and a dot between them.
    DEFAULT_MIN = 3

    # matches the float inside string.
    # example: 0.12, 2.32, 1.0, 0.0, -1.6, 5.06, 101.003, -20.01, 0.000
    # all of these values will be matched.
    # left side of decimal point could not start with '0' if it has more than one digit.
    # values that starting with '+' are not considered as float.
    FLOAT_REGEX = re.compile(r'^[-]?(0|([1-9]([0-9])*))[.]([0-9])+$')

    def __init__(self, **options):
        """
        creates an instance of FloatDeserializer.

        :keyword list[tuple[Pattern, int, int]] accepted_formats: a list of custom accepted
                                                                  formats and their min and
                                                                  max length for float
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

        :rtype: float
        """

        return float(value)

    @property
    def default_formats(self):
        """
        gets default accepted formats that this deserializer could deserialize value from.

        :returns: list[tuple[Pattern format, int min_length, int max_length]]
        :rtype: list[tuple[Pattern, int, int]]
        """

        return [(self.FLOAT_REGEX, self.UNDEF_LENGTH, self.UNDEF_LENGTH)]

# -*- coding: utf-8 -*-
"""
deserializer handlers timedelta module.
"""

import re

from datetime import timedelta

import pyrin.converters.deserializer.services as deserializer_services

from pyrin.core.globals import NULL
from pyrin.converters.deserializer.decorators import deserializer
from pyrin.converters.deserializer.handlers.base import StringPatternDeserializerBase


@deserializer()
class TimedeltaDeserializer(StringPatternDeserializerBase):
    """
    timedelta deserializer class.
    """

    # matches the timedelta definition inside string.
    # example: timedelta(23, 1, 1)
    # it does not support keyword arguments, only positional arguments are supported.
    # matching is case-sensitive.
    TIMEDELTA_REGEX = re.compile(r'^timedelta\([\d, .]*\)$')

    def __init__(self, **options):
        """
        creates an instance of TimedeltaDeserializer.

        :keyword list[tuple[Pattern, int, int]] accepted_formats: a list of custom accepted
                                                                  formats and their min and
                                                                  max length for timedelta
                                                                  deserialization.

        :note accepted_formats: list[tuple[Pattern format, int min_length, int max_length]]
        """

        options.update(internal=True)
        super().__init__(**options)

    def _deserialize(self, value, **options):
        """
        deserializes the given value.

        returns `NULL` object if deserialization fails.
        but if any error occurs, it will be raised.

        :param str value: value to be deserialized.

        :keyword Pattern matching_pattern: the pattern that has matched the value.

        :rtype: timedelta
        """

        args = value.replace('timedelta', '')
        args = deserializer_services.deserialize(args)
        if isinstance(args, tuple):
            return timedelta(*args)

        return NULL

    @property
    def default_formats(self):
        """
        gets default accepted formats that this deserializer could deserialize value from.

        :returns: list[tuple[Pattern format, int min_length, int max_length]]
        :rtype: list[tuple[Pattern, int, int]]
        """

        return [(self.TIMEDELTA_REGEX, 11, self.UNDEF_LENGTH)]

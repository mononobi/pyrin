# -*- coding: utf-8 -*-
"""
deserializer datetime module.
"""

import pyrin.globalization.datetime.services as datetime_services

from pyrin.converters.deserializer.handlers.base import StringPatternDeserializerBase
from pyrin.converters.deserializer.decorators import deserializer
from pyrin.core.globals import NULL
from pyrin.utils.datetime import DEFAULT_DATE_TIME_ISO_REGEX, DEFAULT_DATE_ISO_REGEX, \
    DEFAULT_TIME_ISO_REGEX, DEFAULT_TIME_NO_TIMEZONE_REGEX


@deserializer()
class DateDeserializer(StringPatternDeserializerBase):
    """
    date deserializer class.
    """

    def __init__(self, **options):
        """
        creates an instance of DateDeserializer.

        :keyword list[tuple(Pattern, int)] accepted_formats: a list of custom accepted formats
                                                             and their length for date
                                                             deserialization.

        :type accepted_formats: list[tuple(Pattern format, int length)]
        """

        super().__init__(**options)

    def _deserialize(self, value, **options):
        """
        deserializes the given value.
        returns `NULL` object if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: date
        """

        deserializable, pattern = self.is_deserializable(value, **options)
        if not deserializable:
            return NULL

        value = value.strip()
        converted_date = None

        try:
            converted_date = datetime_services.to_date(value)
            if converted_date is not None:
                return converted_date

            return NULL
        except Exception:
            return NULL

    def get_default_formats(self):
        """
        gets default accepted formats that this
        deserializer could deserialize value from.

        :return: list(tuple(Pattern format, int length))

        :rtype: list(tuple(Pattern, int))
        """

        return [(DEFAULT_DATE_ISO_REGEX, 10)]


@deserializer()
class TimeDeserializer(StringPatternDeserializerBase):
    """
    time deserializer class.
    """

    def __init__(self, **options):
        """
        creates an instance of TimeDeserializer.

        :keyword list[tuple(Pattern, int)] accepted_formats: a list of custom accepted formats
                                                             and their length for time
                                                             deserialization.

        :type accepted_formats: list[tuple(Pattern format, int length)]
        """

        super().__init__(**options)

    def _deserialize(self, value, **options):
        """
        deserializes the given value.
        returns `NULL` object if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: time
        """

        deserializable, pattern = self.is_deserializable(value, **options)
        if not deserializable:
            return NULL

        value = value.strip()
        converted_time = None

        try:
            converted_time = datetime_services.to_time(value)
            if converted_time is not None:
                return converted_time

            return NULL
        except Exception:
            return NULL

    def get_default_formats(self):
        """
        gets default accepted formats that this
        deserializer could deserialize value from.

        :return: list(tuple(Pattern format, int length))

        :rtype: list(tuple(Pattern, int))
        """

        return [(DEFAULT_TIME_ISO_REGEX, 14),
                (DEFAULT_TIME_NO_TIMEZONE_REGEX, 8)]


@deserializer()
class DateTimeDeserializer(StringPatternDeserializerBase):
    """
    datetime deserializer class.
    """

    def __init__(self, **options):
        """
        creates an instance of DateTimeDeserializer.

        :keyword list[tuple(Pattern, int)] accepted_formats: a list of custom accepted formats
                                                             and their length for datetime
                                                             deserialization.

        :type accepted_formats: list[tuple(Pattern format, int length)]
        """

        super().__init__(**options)

    def _deserialize(self, value, **options):
        """
        deserializes the given value.
        returns `NULL` object if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: datetime
        """

        deserializable, pattern = self.is_deserializable(value, **options)
        if not deserializable:
            return NULL

        value = value.strip()
        converted_datetime = None

        try:
            converted_datetime = datetime_services.to_datetime(value)
            if converted_datetime is not None:
                return converted_datetime

            return NULL
        except Exception:
            return NULL

    def get_default_formats(self):
        """
        gets default accepted formats that this
        deserializer could deserialize value from.

        :return: list(tuple(Pattern format, int length))

        :rtype: list(tuple(Pattern, int))
        """

        return [(DEFAULT_DATE_TIME_ISO_REGEX, 25)]

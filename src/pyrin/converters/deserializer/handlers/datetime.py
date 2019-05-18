# -*- coding: utf-8 -*-
"""
deserializer datetime module.
"""

from datetime import date, datetime

from pyrin.converters.deserializer.handlers.base import StringDeserializerBase
from pyrin.converters.deserializer.decorators import deserializer
from pyrin.utils.datetime.converter import DEFAULT_DATE_FORMAT, DEFAULT_TIME_FORMAT_UTC, \
    DEFAULT_DATE_TIME_FORMAT_UTC, to_datetime


@deserializer()
class DateDeserializer(StringDeserializerBase):
    """
    date deserializer class.
    """

    def __init__(self, **options):
        """
        creates an instance of DateDeserializer.

        :keyword list[tuple(str, int)] accepted_formats: a list of custom accepted string
                                                         formats and their length for date
                                                         deserialization.

        :type accepted_formats: list[tuple(str format, int length)]
        """

        StringDeserializerBase.__init__(self, **options)

    def deserialize(self, value, **options):
        """
        deserializes the given value.
        returns None if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: date
        """

        if not self.is_deserializable(value, **options):
            return None

        value = value.strip()
        converted_date = None

        for format_string, length in self.get_accepted_formats():
            try:
                converted_date = to_datetime(value, format=format_string)
                if converted_date is not None:
                    break

                continue
            except ValueError:
                continue

        if converted_date is not None:
            return converted_date.date()

        return converted_date

    @classmethod
    def get_default_formats(cls):
        """
        gets default accepted formats that this
        deserializer could deserialize value from.

        :return: list(tuple(str format, int length))

        :rtype: list(tuple(str, int))
        """

        return [DEFAULT_DATE_FORMAT]


@deserializer()
class TimeDeserializer(StringDeserializerBase):
    """
    time deserializer class.
    """

    def __init__(self, **options):
        """
        creates an instance of TimeDeserializer.

        :keyword list[tuple(str, int)] accepted_formats: a list of all accepted string
                                                         formats and their length for time
                                                         deserialization.

        :type accepted_formats: list[tuple(str format, int length)]
        """

        StringDeserializerBase.__init__(self, **options)

    def deserialize(self, value, **options):
        """
        deserializes the given value.
        returns None if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: time
        """

        if not self.is_deserializable(value, **options):
            return None

        converted_time = None

        for format_string, length in self.get_accepted_formats():
            try:
                converted_time = to_datetime(value, format=format_string)
                if converted_time is not None:
                    break

                continue
            except ValueError:
                continue

        if converted_time is not None:
            return converted_time.timetz()

        return converted_time

    @classmethod
    def get_default_formats(cls):
        """
        gets default accepted formats that this
        deserializer could deserialize value from.

        :return: list(tuple(str format, int length))

        :rtype: list(tuple(str, int))
        """

        return [DEFAULT_TIME_FORMAT_UTC]


@deserializer()
class DateTimeDeserializer(StringDeserializerBase):
    """
    datetime deserializer class.
    """

    def __init__(self, **options):
        """
        creates an instance of DateTimeDeserializer.

        :keyword list[tuple(str, int)] accepted_formats: a list of all accepted string
                                                         formats and their length for date
                                                         deserialization.

        :type accepted_formats: list[tuple(str format, int length)]
        """

        StringDeserializerBase.__init__(self, **options)

    def deserialize(self, value, **options):
        """
        deserializes the given value.
        returns None if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: datetime
        """

        if not self.is_deserializable(value, **options):
            return None

        converted_datetime = None

        for format_string, length in self.get_accepted_formats():
            try:
                converted_datetime = to_datetime(value, format=format_string)
                if converted_datetime is not None:
                    break

                continue
            except ValueError:
                continue

        return converted_datetime

    @classmethod
    def get_default_formats(cls):
        """
        gets default accepted formats that this
        deserializer could deserialize value from.

        :return: list(tuple(str format, int length))

        :rtype: list(tuple(str, int))
        """

        return [DEFAULT_DATE_TIME_FORMAT_UTC]

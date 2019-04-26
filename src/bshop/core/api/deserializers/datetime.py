# -*- coding: utf-8 -*-
"""
Datetime deserializers module.
"""

from datetime import date, datetime

from bshop.core.api.deserializers.base import DeserializerBase
from bshop.core.api.deserializers.decorators import register


@register()
class DateDeserializer(DeserializerBase):
    """
    Date deserializer.
    """

    def __init__(self, **options):
        """
        Creates an instance of DateDeserializer.

        :keyword list[tuple(str, int)] accepted_formats: a list of all accepted string formats
                                                         and their length for date deserialization.
        :type accepted_formats: list[tuple(str: format, int: length)]
        """

        DeserializerBase.__init__(self, **options)

        self._accepted_formats = [('%Y-%m-%d', 10),
                                  ('%Y/%m/%d', 10),
                                  ('%Y.%m.%d', 10)]

        accepted_formats = options.get('accepted_formats', [])
        self._accepted_formats.extend(accepted_formats)

    def deserialize(self, value, **options):
        """
        Deserializes the given value.
        Returns None if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: date
        """

        if value is None or len(value.strip()) == 0:
            return None

        value = value.strip()
        date_length = len(value)
        converted_date = None

        for format_string, length in self._accepted_formats:
            if date_length != length:
                continue

            try:
                converted_date = datetime.strptime(value, format_string)
                if converted_date is not None:
                    break

                continue
            except ValueError:
                continue

        if converted_date is not None:
            return converted_date.date()

        return converted_date


@register()
class TimeDeserializer(DeserializerBase):
    """
    Time deserializer.
    """

    def __init__(self, **options):
        """
        Creates an instance of TimeDeserializer.

        :keyword list[tuple(str, int)] accepted_formats: a list of all accepted string formats
                                                         and their length for time deserialization.
        :type accepted_formats: list[tuple(str: format, int: length)]
        """

        DeserializerBase.__init__(self, **options)

        self._accepted_formats = [('%H:%M:%S%z', 13)]

        accepted_formats = options.get('accepted_formats', [])
        self._accepted_formats.extend(accepted_formats)

    def deserialize(self, value, **options):
        """
        Deserializes the given value.
        Returns None if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: time
        """

        if value is None or len(value.strip()) == 0:
            return None

        value = value.strip()
        time_length = len(value)
        converted_time = None

        for format_string, length in self._accepted_formats:
            if time_length != length:
                continue

            try:
                converted_time = datetime.strptime(value, format_string)
                if converted_time is not None:
                    break

                continue
            except ValueError:
                continue

        if converted_time is not None:
            return converted_time.timetz()

        return converted_time


@register()
class DateTimeDeserializer(DeserializerBase):
    """
    Datetime deserializer.
    """

    def __init__(self, **options):
        """
        Creates an instance of DateTimeDeserializer.

        :keyword list[tuple(str, int)] accepted_formats: a list of all accepted string formats
                                                         and their length for date deserialization.
        :type accepted_formats: list[(str: format, int: length)]
        """

        DeserializerBase.__init__(self, **options)

        self._accepted_formats = [('%Y-%m-%d %H:%M:%S%z', 24),
                                  ('%Y/%m/%d %H:%M:%S%z', 24),
                                  ('%Y.%m.%d %H:%M:%S%z', 24)]

        accepted_formats = options.get('accepted_formats', [])
        self._accepted_formats.extend(accepted_formats)

    def deserialize(self, value, **options):
        """
        Deserializes the given value.
        Returns None if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: datetime
        """

        if value is None or len(value.strip()) == 0:
            return None

        value = value.strip()
        datetime_length = len(value)
        converted_datetime = None

        for format_string, length in self._accepted_formats:
            if datetime_length != length:
                continue

            try:
                converted_datetime = datetime.strptime(value, format_string)
                if converted_datetime is not None:
                    break

                continue
            except ValueError:
                continue

        return converted_datetime

# -*- coding: utf-8 -*-
"""
datetime converter module.
"""

import re
from datetime import datetime


# default datetime format with utc offset.
# example: '2015-12-24 23:40:15+0330'
DEFAULT_DATE_TIME_FORMAT_UTC = ('%Y-%m-%d %H:%M:%S%z', 24)

# default date format.
# example: '2015-12-24'
DEFAULT_DATE_FORMAT = ('%Y-%m-%d', 10)

# default time format with utc offset.
# example: '23:40:15+0330'
DEFAULT_TIME_FORMAT_UTC = ('%H:%M:%S%z', 13)

# default datetime regular expression pattern with utc offset.
# example: '2015-12-24 23:40:15+0330'
DEFAULT_DATE_TIME_UTC_REGEX = re.compile(r'^[1-2]\d{3}-[0-1]\d-[0-3]\d [0-2]\d:[0-5]\d:[0-5]\d[+-][0-1]\d[0-5]\d$')

# default date regular expression pattern.
# example: '2015-12-24'
DEFAULT_DATE_REGEX = re.compile(r'^[1-2]\d{3}-[0-1]\d-[0-3]\d$')

# default time regular expression pattern with utc offset.
# example: '23:40:15+0330'
DEFAULT_TIME_UTC_REGEX = re.compile(r'^[0-2]\d:[0-5]\d:[0-5]\d[+-][0-1]\d[0-5]\d$')


def to_string(value, **options):
    """
    gets the string representation of input value using given format.
    if format is not provided it gives the default datetime format with utc offset.

    :param Union[datetime, date, time] value: input object to be converted.

    :keyword str format: custom format to get string representation of input value.

    :rtype: str
    """

    format_string = options.get('format', DEFAULT_DATE_TIME_FORMAT_UTC[0])
    return value.strftime(format_string)


def to_datetime_string_utc(value):
    """
    gets the utc datetime string representation of input value with utc offset.
    example: `2015-12-24 23:40:15+0330`

    :param Union[datetime, date, time] value: input object to be converted.

    :rtype: str
    """

    return to_string(value, format=DEFAULT_DATE_TIME_FORMAT_UTC[0])


def to_date_string(value):
    """
    gets the date string representation of input with default format.
    example: `2015-12-24`

    :param Union[datetime, date, time] value: input object to be converted.

    :rtype: str
    """

    return to_string(value, format=DEFAULT_DATE_FORMAT[0])


def to_time_string_utc(value):
    """
    gets the utc time string representation of input datetime with utc offset.
    example: `23:40:15+0330`

    :param Union[datetime, date, time] value: input object to be converted.

    :rtype: str
    """

    return to_string(value, format=DEFAULT_TIME_FORMAT_UTC[0])


def to_datetime(value, **options):
    """
    converts the input value to it's equivalent python datetime using the given format.
    if format is not provided it assumes the default datetime format with utc offset.

    :param str value: string representation of datetime to be converted.

    :keyword str format: format of input string.

    :rtype: datetime
    """

    format_string = options.get('format', DEFAULT_DATE_TIME_FORMAT_UTC[0])
    return datetime.strptime(value, format_string)


def to_datetime_utc(value):
    """
    converts the input value to it's equivalent python datetime with utc info
    using default datetime format string with utc offset.

    :param str value: string representation of datetime to be converted.

    :rtype: datetime
    """

    return to_datetime(value, format=DEFAULT_DATE_TIME_FORMAT_UTC[0])


def to_date(value):
    """
    converts the input value to it's equivalent python date using default date format string.

    :param str value: string representation of datetime to be converted.

    :rtype: date
    """

    return to_datetime(value, format=DEFAULT_DATE_FORMAT[0]).date()


def to_time_utc(value):
    """
    converts the input value to it's equivalent python time
    with utc info using default time format string with utc offset.

    :param str value: string representation of datetime to be converted.

    :rtype: time
    """

    return to_datetime(value, format=DEFAULT_TIME_FORMAT_UTC[0]).timetz()

# -*- coding: utf-8 -*-
"""
utils datetime module.
"""

import re

from datetime import datetime, timedelta

import pytz
import aniso8601

import pyrin.globalization.datetime.services as datetime_services


# default iso datetime regular expression pattern with utc offset.
# example: '2015-12-24T23:40:15+03:30'
DEFAULT_DATE_TIME_ISO_REGEX = \
    re.compile(r'^[1-2]\d{3}-[0-1]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d[+-][0-1]\d:[0-5]\d$')

# default iso date regular expression pattern.
# example: '2015-12-24'
DEFAULT_DATE_ISO_REGEX = re.compile(r'^[1-2]\d{3}-[0-1]\d-[0-3]\d$')

# default iso time regular expression pattern with utc offset.
# example: '23:40:15+03:30'
DEFAULT_TIME_ISO_REGEX = re.compile(r'^[0-2]\d:[0-5]\d:[0-5]\d[+-][0-1]\d:[0-5]\d$')

# default iso time regular expression pattern without utc offset.
# example: '23:40:15'
DEFAULT_TIME_NO_TIMEZONE_REGEX = re.compile(r'^[0-2]\d:[0-5]\d:[0-5]\d$')


def to_datetime_string(value):
    """
    gets the datetime string representation of input value with utc offset.
    example: `2015-12-24T23:40:15+03:30`

    :param datetime value: input object to be converted.

    :rtype: str
    """

    return value.isoformat(timespec='seconds')


def to_datetime_string_utc(value):
    """
    gets the datetime string representation of input value in utc with zero offset.
    example: `2015-12-24T22:40:15+00:00`

    :param datetime value: input object to be converted.

    :rtype: str
    """

    utc_value = normalized_utc(value)
    return to_datetime_string(utc_value)


def to_date_string(value):
    """
    gets the date string representation of input with default format.
    example: `2015-12-24`

    :param Union[datetime, date] value: input object to be converted.

    :rtype: str
    """

    date = value
    if isinstance(value, datetime):
        date = value.date()

    return date.isoformat()


def to_time_string(value):
    """
    gets the time string representation of input datetime with utc offset.
    example: `23:40:15`

    :param Union[datetime, time] value: input object to be converted.

    :rtype: str
    """

    time = value
    if isinstance(value, datetime):
        time = value.timetz()

    return time.isoformat(timespec='seconds')


def to_time_string_utc(value):
    """
    gets the time string representation of input datetime in utc with zero offset.
    example: `22:40:15`

    :param Union[datetime, time] value: input object to be converted.

    :rtype: str
    """

    utc_value = normalized_utc(value)
    return to_time_string(utc_value)


def to_datetime(value):
    """
    converts the input value to it's equivalent python datetime.

    :param str value: string representation of datetime to be converted.

    :rtype: datetime
    """

    return aniso8601.parse_datetime(value)


def to_datetime_utc(value):
    """
    converts the input value to it's equivalent python datetime in utc with zero offset.

    :param str value: string representation of datetime to be converted.

    :rtype: datetime
    """

    converted_value = to_datetime(value)
    return normalized_utc(converted_value)


def to_date(value):
    """
    converts the input value to it's equivalent python date.

    :param str value: string representation of date to be converted.

    :rtype: date
    """

    return aniso8601.parse_date(value)


def to_time(value):
    """
    converts the input value to it's equivalent python time.

    :param str value: string representation of time to be converted.

    :rtype: time
    """

    return aniso8601.parse_time(value)


def utc_now():
    """
    gets current datetime in utc timezone with zero offset.

    :rtype: datetime
    """

    dt_now = datetime.utcnow()
    utc = pytz.utc
    return utc.localize(dt_now)


def normalized_utc(value):
    """
    normalizes input datetime value as utc datetime with zero offset and returns it.

    :param datetime value: value to get it's utc equivalent.

    :rtype: datetime
    """

    utc = pytz.utc
    return utc.normalize(value)


def trunc(value):
    """
    truncates the input datetime value to just date, with default time info.
    it is really a datetime with time info set to 00:00:00.

    :param datetime value: datetime to be truncated.

    :rtype: datetime
    """

    return datetime(value.year, value.month, value.day)


def begin_of_day(value):
    """
    gets a datetime representing the begin of day for given datetime.
    it is really a datetime with time info set to 00:00:00.

    :param datetime value: value to get its begin of day.

    :rtype: datetime
    """

    return trunc(value)


def end_of_day(value):
    """
    gets a datetime representing the end of day for given datetime.
    it is really a datetime with time info set to 23:59:59.999999

    :param datetime value: value to get its end of day.

    :rtype: datetime
    """

    return add_days(trunc(value), 1) - timedelta(milliseconds=1)


def add_days(value, days):
    """
    adds the given number of days to specified value and returns it.

    :param datetime value: value to add days to it.

    :param int days: number of days to add.
                     it could be negative if needed.

    :rtype: datetime
    """

    return value + timedelta(days)


def get_current_timestamp():
    """
    gets current time stamp.

    :rtype: str
    """

    current = datetime_services.now()
    return '{year}{month}{day}{hour}{minute}{second}'.format(year=str(current.year).zfill(4),
                                                             month=str(current.month).zfill(2),
                                                             day=str(current.day).zfill(2),
                                                             hour=str(current.hour).zfill(2),
                                                             minute=str(current.minute).zfill(2),
                                                             second=str(current.second).zfill(2))

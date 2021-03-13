# -*- coding: utf-8 -*-
"""
utils datetime module.
"""

import re

from datetime import datetime, timedelta, date

import pytz
import aniso8601

import pyrin.security.session.services as session_services


# default iso datetime regular expression pattern with utc offset.
# example: '2015-12-24T23:40:15+03:30' or '2015-12-24T23:40:15.8965+03:30'
# length is between 25 to 32.
DEFAULT_DATE_TIME_ISO_REGEX = \
    re.compile(
        r'^[1-2]\d{3}-[0-1]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d(\.\d{1,6})?[+-][0-1]\d:[0-5]\d$')

# default iso date regular expression pattern.
# example: '2015-12-24'
# length is 10.
DEFAULT_DATE_ISO_REGEX = re.compile(r'^[1-2]\d{3}-[0-1]\d-[0-3]\d$')

# default utc datetime regular expression pattern with zulu sign.
# example: '2015-12-24T23:40:15.926Z' or '2015-12-24T23:40:15Z'
# length is between 20 to 27.
DEFAULT_UTC_ZULU_DATE_TIME_REGEX = \
    re.compile(r'^[1-2]\d{3}-[0-1]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d(\.\d{1,6})?Z$')

# default iso time regular expression pattern with utc offset.
# example: '23:40:15+03:30' or '23:40:15.889+03:30'
# length is between 14 to 21.
DEFAULT_TIME_ISO_REGEX = re.compile(r'^[0-2]\d:[0-5]\d:[0-5]\d(\.\d{1,6})?[+-][0-1]\d:[0-5]\d$')

# default local naive datetime regular expression pattern without utc offset.
# example: '2015-12-24T23:40:15' or '2015-12-24T23:40:15.98'
# length is between 19 to 26.
DEFAULT_LOCAL_NAIVE_DATE_TIME_REGEX = \
    re.compile(r'^[1-2]\d{3}-[0-1]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d(\.\d{1,6})?$')

# default local naive time regular expression pattern without utc offset.
# example: '23:40:15' or '23:40:15.565'
# length is between 8 to 15.
DEFAULT_LOCAL_NAIVE_TIME_REGEX = re.compile(r'^[0-2]\d:[0-5]\d:[0-5]\d(\.\d{1,6})?$')


def to_datetime_string(value):
    """
    gets the datetime string representation of input value with utc offset.

    for example: `2015-12-24T23:40:15+03:30`

    :param datetime value: input object to be converted.

    :rtype: str
    """

    return value.isoformat(timespec='seconds')


def to_datetime_string_utc(value):
    """
    gets the datetime string representation of input value in utc with zero offset.

    for example: `2015-12-24T22:40:15+00:00`

    :param datetime value: input object to be converted.

    :rtype: str
    """

    utc_value = normalized_utc(value)
    return to_datetime_string(utc_value)


def to_date_string(value):
    """
    gets the date string representation of input with default format.

    for example: `2015-12-24`

    :param datetime | date value: input object to be converted.

    :rtype: str
    """

    date = value
    if isinstance(value, datetime):
        date = value.date()

    return date.isoformat()


def to_time_string(value):
    """
    gets the time string representation of input datetime with utc offset.

    for example: `23:40:15`

    :param datetime | time value: input object to be converted.

    :rtype: str
    """

    time = value
    if isinstance(value, datetime):
        time = value.timetz()

    return time.isoformat(timespec='seconds')


def to_time_string_utc(value):
    """
    gets the time string representation of input datetime in utc with zero offset.

    for example: `22:40:15`

    :param datetime | time value: input object to be converted.

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


def to_datetime_from_date(value):
    """
    converts the input date to it's equivalent python datetime.

    the time info will be set to `00:00:00`.

    :param date value: date value to be converted.

    :rtype: datetime
    """

    return datetime(year=value.year, month=value.month, day=value.day)


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

    it is actually a datetime with time info set to 00:00:00.

    :param datetime | date value: value to be truncated.

    :rtype: datetime
    """

    tz = None
    if isinstance(value, datetime) and value.tzinfo is not None:
        tz = value.tzinfo

    if tz is None:
        current_request = session_services.get_safe_current_request()
        if current_request is not None:
            tz = current_request.timezone

    result = datetime(value.year, value.month, value.day, tzinfo=None)
    if tz is None:
        return result

    return tz.localize(result)


def begin_of_day(value):
    """
    gets a datetime representing the begin of day for given datetime.

    it is actually a datetime with time info set to 00:00:00.

    :param datetime | date value: value to get its begin of day.

    :rtype: datetime
    """

    return trunc(value)


def end_of_day(value):
    """
    gets a datetime representing the end of day for given datetime.

    it is actually a datetime with time info set to 23:59:59.999.

    :param datetime | date value: value to get its end of day.

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


def normalize_datetime_range(value_lower, value_upper, **options):
    """
    normalizes the given datetime values range.

    it returns a tuple of two datetime values
    normalized according to given options.

    if the inputs are date objects, they will be converted to datetime with client
    timezone and `consider_begin_of_day` and `consider_end_of_day` will also
    considered as True.

    :param datetime | date value_lower: lower bound of datetime range.
    :param datetime | date value_upper: upper bound of datetime range.

    :keyword bool consider_begin_of_day: specifies that consider begin
                                         of day for lower datetime.
                                         defaults to False if not provided.

    :keyword bool consider_end_of_day: specifies that consider end
                                       of day for upper datetime.
                                       defaults to False if not provided.

    :returns: tuple[datetime value_lower: datetime value_upper]
    :rtype: tuple[datetime, datetime]
    """

    consider_begin_of_day = options.get('consider_begin_of_day', False)
    consider_end_of_day = options.get('consider_end_of_day', False)

    if value_lower is not None and not isinstance(value_lower, datetime):
        consider_begin_of_day = True
        value_lower = to_datetime_from_date(value_lower)

    if value_upper is not None and not isinstance(value_upper, datetime):
        consider_end_of_day = True
        value_upper = to_datetime_from_date(value_upper)

    # swapping values in case of user mistake.
    if value_lower is not None and value_upper is not None:
        lower_has_timezone = value_lower.tzinfo is not None
        upper_has_timezone = value_upper.tzinfo is not None

        if lower_has_timezone is upper_has_timezone and value_lower > value_upper:
            value_lower, value_upper = value_upper, value_lower

    if value_lower is not None and consider_begin_of_day is True:
        value_lower = begin_of_day(value_lower)

    if value_upper is not None and consider_end_of_day is True:
        value_upper = end_of_day(value_upper)

    return value_lower, value_upper


def coerce_to_begin_of_day_datetime(value):
    """
    gets the begin of day datetime equivalent of given date object.

    if the value is not a date, it returns the same input.

    :param date value: value to be coerced.

    :rtype: datetime | object
    """

    if not isinstance(value, datetime) and isinstance(value, date):
        return begin_of_day(value)

    return value


def coerce_to_end_of_day_datetime(value):
    """
    gets the end of day datetime equivalent of given date object.

    if the value is not a date, it returns the same input.

    :param date value: value to be coerced.

    :rtype: datetime | object
    """

    if not isinstance(value, datetime) and isinstance(value, date):
        return end_of_day(value)

    return value

# -*- coding: utf-8 -*-
"""
datetime services module.
"""

from pyrin.application.services import get_component
from pyrin.globalization.datetime import DateTimePackage


def now(timezone=None):
    """
    gets the current datetime based on given timezone name.

    :param str timezone: timezone name to get current datetime based on it.
                         if not provided, defaults to application
                         current timezone.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).now(timezone)


def get_current_timezone():
    """
    gets the application current timezone.

    :rtype: tzinfo
    """

    return get_component(DateTimePackage.COMPONENT_NAME).get_current_timezone()


def get_current_timezone_name():
    """
    gets the application current timezone name.

    :rtype: str
    """

    return get_component(DateTimePackage.COMPONENT_NAME).get_current_timezone_name()


def normalize(value):
    """
    normalizes input datetime value using application current timezone.
    input value should already have a timezone info.

    :param datetime value: value to get normalized.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).normalize(value)


def localize(value):
    """
    localizes input datetime with application current timezone.
    input value should not have a timezone info.

    :param datetime value: value to be localized.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).localize(value)


def to_datetime_string(value):
    """
    gets the datetime string representation of input value.
    if the value has no timezone info, it adds the application
    current timezone info into it.
    example: `2015-12-24T22:40:15+01:00`

    :param datetime value: input object to be converted.

    :rtype: str
    """

    return get_component(DateTimePackage.COMPONENT_NAME).to_datetime_string(value)


def to_date_string(value):
    """
    gets the date string representation of input value.
    example: `2015-12-24`

    :param Union[datetime, date] value: input object to be converted.

    :rtype: str
    """

    return get_component(DateTimePackage.COMPONENT_NAME).to_date_string(value)


def to_time_string(value):
    """
    gets the time string representation of input value.
    if the value has no timezone info, it adds the application
    current timezone info into it.
    example: `23:40:15`

    :param Union[datetime, time] value: input object to be converted.

    :rtype: str
    """

    return get_component(DateTimePackage.COMPONENT_NAME).to_time_string(value)


def to_datetime(value):
    """
    converts the input value to it's equivalent python datetime.

    :param str value: string representation of datetime to be converted.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).to_datetime(value)


def to_date(value):
    """
    converts the input value to it's equivalent python date.

    :param str value: string representation of date to be converted.

    :rtype: date
    """

    return get_component(DateTimePackage.COMPONENT_NAME).to_date(value)


def to_time(value):
    """
    converts the input value to it's equivalent python time.

    :param str value: string representation of time to be converted.

    :rtype: time
    """

    return get_component(DateTimePackage.COMPONENT_NAME).to_time(value)


def timezone_exists(timezone_name):
    """
    gets a value indicating that a timezone with the given name exists.

    :param str timezone_name: timezone name to check for existence.

    :rtype: bool
    """

    return get_component(DateTimePackage.COMPONENT_NAME).timezone_exists(timezone_name)


def get_current_timestamp(date_sep='-', main_sep=' ',
                          time_sep=':', timezone=None):
    """
    gets the current timestamp with specified separators based on given timezone.

    :param Union[str, None] date_sep: a separator to put between date elements.
    :param Union[str, None] main_sep: a separator to put between date and time part.
    :param Union[str, None] time_sep: a separator to put between time elements.

    :param Union[str, None] timezone: timezone name to get current timestamp
                                      based on it. if not provided, defaults
                                      to application current timezone.

    :rtype: str
    """

    return get_component(DateTimePackage.COMPONENT_NAME).get_current_timestamp(date_sep,
                                                                               main_sep,
                                                                               time_sep,
                                                                               timezone)

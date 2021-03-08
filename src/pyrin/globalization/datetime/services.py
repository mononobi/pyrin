# -*- coding: utf-8 -*-
"""
datetime services module.
"""

from pyrin.application.services import get_component
from pyrin.globalization.datetime import DateTimePackage


def now(server=True, timezone=None):
    """
    gets the current datetime based on requested timezone.

    :param bool server: if set to True, server timezone will be used.
                        if set to False, client timezone will be used.
                        defaults to True.

    :param str timezone: timezone name to get datetime based on it.
                         if provided, the value of `server` input
                         will be ignored. defaults to None.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).now(server, timezone)


def client_now():
    """
    gets the current datetime based on client timezone.

    this is a helper method to let get the client datetime
    without providing value to `now` method.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).client_now()


def today(server=True, timezone=None):
    """
    gets the current date based on requested timezone.

    :param bool server: if set to True, server timezone will be used.
                        if set to False, client timezone will be used.
                        defaults to True.

    :param str timezone: timezone name to get date based on it.
                         if provided, the value of `server` input
                         will be ignored. defaults to None.

    :rtype: date
    """

    return get_component(DateTimePackage.COMPONENT_NAME).today(server, timezone)


def client_today():
    """
    gets the current date based on client timezone.

    this is a helper method to let get the client date
    without providing value to `today` method.

    :rtype: date
    """

    return get_component(DateTimePackage.COMPONENT_NAME).client_today()


def current_year(server=True, timezone=None):
    """
    gets the current year based on requested timezone.

    :param bool server: if set to True, server timezone will be used.
                        if set to False, client timezone will be used.
                        defaults to True.

    :param str timezone: timezone name to get year based on it.
                         if provided, the value of `server` input
                         will be ignored. defaults to None.

    :rtype: int
    """

    return get_component(DateTimePackage.COMPONENT_NAME).current_year(server, timezone)


def current_client_year():
    """
    gets the current year based on client timezone.

    this is a helper method to let get the client year
    without providing value to `current_year` method.

    :rtype: int
    """

    return get_component(DateTimePackage.COMPONENT_NAME).current_client_year()


def get_default_client_timezone():
    """
    gets the default client timezone.

    :rtype: tzinfo
    """

    return get_component(DateTimePackage.COMPONENT_NAME).get_default_client_timezone()


def get_current_timezone(server):
    """
    gets the current timezone for server or client.

    :param bool server: if set to True, server timezone will be returned.
                        if set to False, client timezone will be returned.

    :rtype: tzinfo
    """

    return get_component(DateTimePackage.COMPONENT_NAME).get_current_timezone(server)


def get_timezone(timezone):
    """
    gets the timezone based on given timezone name.

    :param str timezone: timezone name.

    :rtype: tzinfo
    """

    return get_component(DateTimePackage.COMPONENT_NAME).get_timezone(timezone)


def get_timezone_name(server):
    """
    gets the server or client timezone name.

    :param bool server: if set to True, server timezone name will be returned.
                        if set to False, client timezone name will be returned.

    :rtype: str
    """

    return get_component(DateTimePackage.COMPONENT_NAME).get_timezone_name(server)


def convert(value, to_server, from_server=None):
    """
    converts the given datetime between server and client timezones.

    :param datetime value: value to be converted.

    :param bool to_server: specifies that value must be normalized
                           to server timezone. if set to False, it
                           will be normalized to client timezone.

    :param bool from_server: specifies that value must be normalized
                             from server timezone. if set to False, it
                             will be normalized from client timezone.
                             if not provided, it will be set to opposite
                             of `to_server` value.
    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).convert(value, to_server,
                                                                 from_server=from_server)


def convert_to_utc(value, from_server):
    """
    converts the given datetime to utc.

    :param datetime value: value to be converted.

    :param bool from_server: specifies that value must be normalized
                             from server timezone. if set to False, it
                             will be normalized from client timezone.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).convert_to_utc(value, from_server)


def convert_from_utc(value, to_server):
    """
    converts the given datetime from utc.

    :param datetime value: value to be converted.

    :param bool to_server: specifies that value must be normalized
                           to server timezone. if set to False, it
                           will be normalized to client timezone.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).convert_from_utc(value, to_server)


def as_timezone(value, server):
    """
    gets the result of `astimezone` on the given value.

    :param datetime value: value to get normalized.

    :param bool server: if set to True, server timezone name will be used.
                        if set to False, client timezone name will be used.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).as_timezone(value, server)


def normalize(value, server):
    """
    normalizes input value using server or client current timezone and returns it.

    :param datetime value: value to get normalized.
    :param bool server: specifies that server or client timezone must used.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).normalize(value, server)


def localize(value, server):
    """
    localizes input datetime with current timezone.

    input value should not have a timezone info.

    :param datetime value: value to be localized.
    :param bool server: specifies that server or client timezone must used.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).localize(value, server)


def try_add_timezone(value, server):
    """
    adds the current timezone info into input value if it has no timezone info.

    :param datetime value: value to add timezone info into it.
    :param bool server: specifies that server or client timezone must be added.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).try_add_timezone(value, server)


def to_datetime_string(value, to_server, from_server=None):
    """
    gets the datetime string representation of input value.

    if the value has no timezone info, it adds the client or server
    timezone info based on `from_server` value.

    example: `2015-12-24T22:40:15+01:00`

    :param datetime value: input object to be converted.

    :param bool to_server: specifies that value must be normalized
                           to server timezone. if set to False, it
                           will be normalized to client timezone.

    :param bool from_server: specifies that value must be normalized
                             from server timezone. if set to False, it
                             will be normalized from client timezone.
                             if not provided, it will be set to opposite
                             of `to_server` value.

    :rtype: str
    """

    return get_component(DateTimePackage.COMPONENT_NAME).to_datetime_string(
        value, to_server, from_server=from_server)


def to_date_string(value):
    """
    gets the date string representation of input value.

    example: `2015-12-24`

    :param datetime | date value: input object to be converted.

    :rtype: str
    """

    return get_component(DateTimePackage.COMPONENT_NAME).to_date_string(value)


def to_time_string(value, to_server, from_server=None):
    """
    gets the time string representation of input value.

    if the value is a datetime and has no timezone info, it adds
    the client or server timezone info based on `from_server` value.

    example: `23:40:15`

    :param datetime | time value: input object to be converted.

    :param bool to_server: specifies that value must be normalized
                           to server timezone. if set to False, it
                           will be normalized to client timezone.

    :param bool from_server: specifies that value must be normalized
                             from server timezone. if set to False, it
                             will be normalized from client timezone.
                             if not provided, it will be set to opposite
                             of `to_server` value.

    :rtype: str
    """

    return get_component(DateTimePackage.COMPONENT_NAME).to_time_string(value, to_server,
                                                                        from_server=from_server)


def to_datetime(value, to_server, from_server=None):
    """
    converts the input value to it's equivalent python datetime.

    if the value has no timezone info, it adds the client or server
    timezone info based on `from_server` value.

    :param str value: string representation of datetime to be converted.

    :param bool to_server: specifies that value must be normalized
                           to server timezone. if set to False, it
                           will be normalized to client timezone.

    :param bool from_server: specifies that value must be normalized
                             from server timezone. if set to False, it
                             will be normalized from client timezone.
                             if not provided, it will be set to opposite
                             of `to_server` value.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).to_datetime(value, to_server,
                                                                     from_server=from_server)


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


def get_timestamp(value, date_sep='-', main_sep=' ',
                  time_sep=':', microsecond=False):
    """
    gets the timestamp with specified separators for given datetime.

    default format is `YYYY-MM-DD HH:mm:SS`.

    :param datetime value: datetime value to get its timestamp.

    :param str date_sep: a separator to put between date elements.
                         if set to None, no separator will be used.

    :param str main_sep: a separator to put between date and time part.
                         if set to None, no separator will be used.

    :param str time_sep: a separator to put between time elements.
                         if set to None, no separator will be used.

    :param bool microsecond: specifies that timestamp must include microseconds.
                             defaults to False if not provided.

    :rtype: str
    """

    return get_component(DateTimePackage.COMPONENT_NAME).get_timestamp(value, date_sep,
                                                                       main_sep, time_sep,
                                                                       microsecond)


def get_current_timestamp(date_sep='-', main_sep=' ',
                          time_sep=':', server=True,
                          timezone=None, microsecond=False):
    """
    gets the current timestamp with specified separators based on requested timezone.

    default format is `YYYY-MM-DD HH:mm:SS`.

    :param str date_sep: a separator to put between date elements.
                         if set to None, no separator will be used.

    :param str main_sep: a separator to put between date and time part.
                         if set to None, no separator will be used.

    :param str time_sep: a separator to put between time elements.
                         if set to None, no separator will be used.

    :param bool server: if set to True, server timezone will be used.
                        if set to False, client timezone will be used.
                        defaults to True.

    :param str timezone: timezone name to get datetime based on it.
                         if provided, the value of `server` input
                         will be ignored. defaults to None.

    :param bool microsecond: specifies that timestamp must include microseconds.
                             defaults to False if not provided.

    :rtype: str
    """

    return get_component(DateTimePackage.COMPONENT_NAME).get_current_timestamp(date_sep,
                                                                               main_sep,
                                                                               time_sep,
                                                                               server,
                                                                               timezone,
                                                                               microsecond)


def datetime(year, month, day, hour=0, minute=0,
             second=0, microsecond=0, fold=0,
             server=True, timezone=None):
    """
    gets a new datetime with given inputs and requested timezone.

    :param int year: year.
    :param int month: month.
    :param int day: day.
    :param int hour: hour.
    :param int minute: minute.
    :param int second: second.
    :param int microsecond: microsecond.

    :param int fold: used to disambiguate wall times during a repeated
                     interval. it could be set to 0 or 1.

    :param bool server: if set to True, server timezone will be used.
                        if set to False, client timezone will be used.
                        defaults to True.

    :param str timezone: timezone name to be used.
                         if provided, the value of `server` input
                         will be ignored. defaults to None.
    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).datetime(year, month, day,
                                                                  hour, minute, second,
                                                                  microsecond, fold,
                                                                  server, timezone)

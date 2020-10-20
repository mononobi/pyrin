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


def replace_timezone(value, server):
    """
    replaces given value's timezone with server or client timezone.

    it returns a new object.
    note that this method does not normalize the value, it just replaces the
    timezone and localizes the value.

    :param datetime value: value to replace its timezone.
    :param bool server: specifies that server or client timezone must used.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).replace_timezone(value, server)


def to_datetime_string(value, server):
    """
    gets the datetime string representation of input value.

    if the value has no timezone info, it adds the client or server
    timezone info based on `server` value.

    example: `2015-12-24T22:40:15+01:00`

    :param datetime value: input object to be converted.

    :param bool server: specifies that value must be normalized
                        to server or client timezone.

    :rtype: str
    """

    return get_component(DateTimePackage.COMPONENT_NAME).to_datetime_string(value, server)


def to_date_string(value):
    """
    gets the date string representation of input value.

    example: `2015-12-24`

    :param datetime | date value: input object to be converted.

    :rtype: str
    """

    return get_component(DateTimePackage.COMPONENT_NAME).to_date_string(value)


def to_time_string(value, server):
    """
    gets the time string representation of input value.

    if the value is a datetime and has no timezone info, it adds
    the client or server timezone info based on `server` value.

    example: `23:40:15`

    :param datetime | time value: input object to be converted.

    :param bool server: specifies that value must be normalized
                        to server or client timezone.

    :rtype: str
    """

    return get_component(DateTimePackage.COMPONENT_NAME).to_time_string(value, server)


def to_datetime(value, server, replace_server=None):
    """
    converts the input value to it's equivalent python datetime.

    :param str value: string representation of datetime to be converted.

    :param bool server: specifies that value must be normalized
                        to server or client timezone.

    :param bool replace_server: specifies that it must replace the timezone
                                of value with timezone of server before
                                normalization. if set to False, it replaces
                                it with client timezone.
                                defaults to None and no replacement will be done.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).to_datetime(value, server,
                                                                     replace_server)


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
                          time_sep=':', server=True, timezone=None):
    """
    gets the current timestamp with specified separators based on requested timezone.

    :param str date_sep: a separator to put between date elements.
    :param str main_sep: a separator to put between date and time part.
    :param str time_sep: a separator to put between time elements.

    :param bool server: if set to True, server timezone will be used.
                        if set to False, client timezone will be used.
                        defaults to True.

    :param str timezone: timezone name to get datetime based on it.
                         if provided, the value of `server` input
                         will be ignored. defaults to None.

    :rtype: str
    """

    return get_component(DateTimePackage.COMPONENT_NAME).get_current_timestamp(date_sep,
                                                                               main_sep,
                                                                               time_sep,
                                                                               server,
                                                                               timezone)

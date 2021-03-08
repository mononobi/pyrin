# -*- coding: utf-8 -*-
"""
datetime manager module.
"""

from datetime import datetime, date

import pytz

import pyrin.configuration.services as config_services
import pyrin.security.session.services as session_services
import pyrin.utils.datetime as datetime_utils

from pyrin.core.structs import Manager
from pyrin.globalization.datetime import DateTimePackage
from pyrin.globalization.datetime.enumerations import TimezoneEnum


class DateTimeManager(Manager):
    """
    datetime manager class.
    """

    package_class = DateTimePackage

    def __init__(self, **options):
        """
        initializes an instance of DateTimeManager.
        """

        super().__init__()

        server_timezone = config_services.get('globalization',
                                              'locale', 'babel_default_timezone')

        client_timezone = config_services.get('globalization', 'locale', 'client_timezone')

        self._server_timezone = self.get_timezone(server_timezone)
        self._client_timezone = self.get_timezone(client_timezone)

    def _try_add_timezone(self, value, timezone):
        """
        adds the given timezone info into input value if it has no timezone info.

        :param datetime value: value to add timezone info into it.
        :param str timezone: timezone name to get datetime based on it.

        :rtype: datetime
        """

        localized_value = value
        if value.tzinfo is None:
            localized_value = self._localize(value, timezone)

        return localized_value

    def _localize(self, value, timezone):
        """
        localizes input datetime with given timezone.

        input value should not have a timezone info.

        :param datetime value: value to be localized.
        :param str timezone: timezone name to get datetime based on it.

        :rtype: datetime
        """

        timezone = self.get_timezone(timezone)
        return timezone.localize(value)

    def _as_timezone(self, value, timezone):
        """
        gets the result of `astimezone` on the given value.

        :param datetime value: value to get normalized.
        :param str timezone: timezone name to get datetime based on it.

        :rtype: datetime
        """

        timezone = self.get_timezone(timezone)
        return value.astimezone(timezone)

    def _normalize(self, value, timezone):
        """
        normalizes input value using given timezone and returns it.

        :param datetime value: value to get normalized.
        :param str timezone: timezone name to get datetime based on it.

        :rtype: datetime
        """

        value = self._as_timezone(value, timezone)
        timezone = self.get_timezone(timezone)
        return timezone.normalize(value)

    def now(self, server=True, timezone=None):
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

        if timezone not in (None, ''):
            timezone = self.get_timezone(timezone)
        else:
            timezone = self.get_current_timezone(server=server)

        return datetime.now(timezone)

    def client_now(self):
        """
        gets the current datetime based on client timezone.

        this is a helper method to let get the client datetime
        without providing value to `now` method.

        :rtype: datetime
        """

        return self.now(server=False)

    def today(self, server=True, timezone=None):
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

        now = self.now(server, timezone=timezone)
        return date(year=now.year, month=now.month, day=now.day)

    def client_today(self):
        """
        gets the current date based on client timezone.

        this is a helper method to let get the client date
        without providing value to `today` method.

        :rtype: date
        """

        return self.today(server=False)

    def current_year(self, server=True, timezone=None):
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

        now = self.now(server=server, timezone=timezone)
        return now.year

    def current_client_year(self):
        """
        gets the current year based on client timezone.

        this is a helper method to let get the client year
        without providing value to `current_year` method.

        :rtype: int
        """

        client_now = self.client_now()
        return client_now.year

    def get_default_client_timezone(self):
        """
        gets the default client timezone.

        :rtype: tzinfo
        """

        return self._client_timezone

    def get_current_timezone(self, server):
        """
        gets the current timezone for server or client.

        :param bool server: if set to True, server timezone will be returned.
                            if set to False, client timezone will be returned.

        :rtype: tzinfo
        """

        if server is True:
            return self._server_timezone
        else:
            request = session_services.get_safe_current_request()
            timezone = None
            if request is not None:
                timezone = request.timezone

            return timezone or self._client_timezone

    def get_timezone(self, timezone):
        """
        gets the timezone based on given timezone name.

        :param str timezone: timezone name.

        :rtype: tzinfo
        """

        return pytz.timezone(timezone)

    def get_timezone_name(self, server):
        """
        gets the server or client timezone name.

        :param bool server: if set to True, server timezone name will be returned.
                            if set to False, client timezone name will be returned.

        :rtype: str
        """

        return self.get_current_timezone(server).zone

    def convert(self, value, to_server, from_server=None):
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

        if from_server is None:
            from_server = not to_server

        localized_value = self.try_add_timezone(value, server=from_server)
        return self.normalize(localized_value, server=to_server)

    def convert_to_utc(self, value, from_server):
        """
        converts the given datetime to utc.

        :param datetime value: value to be converted.

        :param bool from_server: specifies that value must be normalized
                                 from server timezone. if set to False, it
                                 will be normalized from client timezone.

        :rtype: datetime
        """

        localized_value = self.try_add_timezone(value, server=from_server)
        return self._normalize(localized_value, TimezoneEnum.UTC)

    def convert_from_utc(self, value, to_server):
        """
        converts the given datetime from utc.

        :param datetime value: value to be converted.

        :param bool to_server: specifies that value must be normalized
                               to server timezone. if set to False, it
                               will be normalized to client timezone.

        :rtype: datetime
        """

        localized_value = self._try_add_timezone(value, TimezoneEnum.UTC)
        return self.normalize(localized_value, to_server)

    def as_timezone(self, value, server):
        """
        gets the result of `astimezone` on the given value.

        :param datetime value: value to get normalized.

        :param bool server: if set to True, server timezone name will be used.
                            if set to False, client timezone name will be used.

        :rtype: datetime
        """

        timezone = self.get_timezone_name(server=server)
        return self._as_timezone(value, timezone)

    def normalize(self, value, server):
        """
        normalizes input value using server or client current timezone and returns it.

        :param datetime value: value to get normalized.
        :param bool server: specifies that server or client timezone must used.

        :rtype: datetime
        """

        timezone = self.get_timezone_name(server)
        return self._normalize(value, timezone)

    def localize(self, value, server):
        """
        localizes input datetime with current timezone.

        input value should not have a timezone info.

        :param datetime value: value to be localized.
        :param bool server: specifies that server or client timezone must used.

        :rtype: datetime
        """

        timezone = self.get_timezone_name(server)
        return self._localize(value, timezone)

    def try_add_timezone(self, value, server):
        """
        adds the current timezone info into input value if it has no timezone info.

        :param datetime value: value to add timezone info into it.
        :param bool server: specifies that server or client timezone must be added.

        :rtype: datetime
        """

        timezone = self.get_timezone_name(server)
        return self._try_add_timezone(value, timezone)

    def to_datetime_string(self, value, to_server, from_server=None):
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

        localized_value = self.convert(value, to_server, from_server=from_server)
        return datetime_utils.to_datetime_string(localized_value)

    def to_date_string(self, value):
        """
        gets the date string representation of input value.

        example: `2015-12-24`

        :param datetime | date value: input object to be converted.

        :rtype: str
        """

        return datetime_utils.to_date_string(value)

    def to_time_string(self, value, to_server, from_server=None):
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

        localized_value = value
        if isinstance(value, datetime):
            localized_value = self.convert(value, to_server, from_server=from_server)

        return datetime_utils.to_time_string(localized_value)

    def to_datetime(self, value, to_server, from_server=None):
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

        converted_datetime = datetime_utils.to_datetime(value)
        return self.convert(converted_datetime, to_server, from_server=from_server)

    def to_date(self, value):
        """
        converts the input value to it's equivalent python date.

        :param str value: string representation of date to be converted.

        :rtype: date
        """

        return datetime_utils.to_date(value)

    def to_time(self, value):
        """
        converts the input value to it's equivalent python time.

        :param str value: string representation of time to be converted.

        :rtype: time
        """

        return datetime_utils.to_time(value)

    def timezone_exists(self, timezone_name):
        """
        gets a value indicating that a timezone with the given name exists.

        :param str timezone_name: timezone name to check for existence.

        :rtype: bool
        """

        return timezone_name in pytz.all_timezones_set

    def get_timestamp(self, value, date_sep='-', main_sep=' ',
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

        if date_sep is None:
            date_sep = ''
        if main_sep is None:
            main_sep = ''
        if time_sep is None:
            time_sep = ''

        place_holder = '{year}{date_sep}{month}{date_sep}{day}{main_sep}' \
                       '{hour}{time_sep}{minute}{time_sep}{second}'

        if microsecond is True:
            place_holder = place_holder + '.{microsecond}'

        return place_holder.format(year=str(value.year).zfill(4),
                                   month=str(value.month).zfill(2),
                                   day=str(value.day).zfill(2),
                                   hour=str(value.hour).zfill(2),
                                   minute=str(value.minute).zfill(2),
                                   second=str(value.second).zfill(2),
                                   date_sep=date_sep,
                                   main_sep=main_sep,
                                   time_sep=time_sep,
                                   microsecond=value.microsecond)

    def get_current_timestamp(self, date_sep='-', main_sep=' ',
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

        current = self.now(server=server, timezone=timezone)
        return self.get_timestamp(current, date_sep=date_sep, main_sep=main_sep,
                                  time_sep=time_sep, microsecond=microsecond)

    def datetime(self, year, month, day, hour=0, minute=0,
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

        result = datetime(year=year, month=month, day=day, hour=hour, minute=minute,
                          second=second, microsecond=microsecond, fold=fold)

        if timezone not in (None, ''):
            return self._try_add_timezone(result, timezone)

        return self.try_add_timezone(result, server)

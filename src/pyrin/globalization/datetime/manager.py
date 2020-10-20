# -*- coding: utf-8 -*-
"""
datetime manager module.
"""

from datetime import datetime

import pytz

import pyrin.configuration.services as config_services
import pyrin.security.session.services as session_services
import pyrin.utils.datetime as datetime_utils

from pyrin.core.structs import Manager
from pyrin.globalization.datetime import DateTimePackage


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

        client_timezone = config_services.get('globalization',
                                              'locale', 'client_timezone')

        self._server_timezone = pytz.timezone(server_timezone)
        self._client_timezone = pytz.timezone(client_timezone)

    def _add_timezone(self, value, server):
        """
        adds the current timezone info into input value if it has no timezone info.

        :param datetime value: value to add timezone info into it.
        :param bool server: specifies that server or client timezone must be added.

        :rtype: datetime
        """

        localized_value = value
        if value.tzinfo is None:
            localized_value = self.localize(value, server=server)

        return localized_value

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

    def as_timezone(self, value, server):
        """
        gets the result of `astimezone` on the given value.

        :param datetime value: value to get normalized.

        :param bool server: if set to True, server timezone name will be used.
                            if set to False, client timezone name will be used.

        :rtype: datetime
        """

        timezone = self.get_current_timezone(server=server)
        return value.astimezone(timezone)

    def normalize(self, value, server):
        """
        normalizes input value using server or client current timezone and returns it.

        :param datetime value: value to get normalized.
        :param bool server: specifies that server or client timezone must used.

        :rtype: datetime
        """

        value = self.as_timezone(value, server=server)
        return self.get_current_timezone(server).normalize(value)

    def localize(self, value, server):
        """
        localizes input datetime with current timezone.

        input value should not have a timezone info.

        :param datetime value: value to be localized.
        :param bool server: specifies that server or client timezone must used.

        :rtype: datetime
        """

        return self.get_current_timezone(server).localize(value)

    def replace_timezone(self, value, server):
        """
        replaces given value's timezone with server or client timezone.

        it returns a new object.
        note that this method does not normalize the value, it just replaces the
        timezone and localizes the value.

        :param datetime value: value to replace its timezone.
        :param bool server: specifies that server or client timezone must used.

        :rtype: datetime
        """

        value = value.replace(tzinfo=None)
        return self.localize(value, server)

    def to_datetime_string(self, value, server):
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

        localized_value = self._add_timezone(value, server=server)
        localized_value = self.normalize(localized_value, server=server)
        return datetime_utils.to_datetime_string(localized_value)

    def to_date_string(self, value):
        """
        gets the date string representation of input value.

        example: `2015-12-24`

        :param datetime | date value: input object to be converted.

        :rtype: str
        """

        return datetime_utils.to_date_string(value)

    def to_time_string(self, value, server):
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

        localized_value = value
        if isinstance(value, datetime):
            localized_value = self._add_timezone(value, server=server)
            localized_value = self.normalize(localized_value, server=server)

        return datetime_utils.to_time_string(localized_value)

    def to_datetime(self, value, server, replace_server=None):
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

        converted_datetime = datetime_utils.to_datetime(value)
        if replace_server is not None:
            converted_datetime = self.replace_timezone(converted_datetime, replace_server)

        converted_datetime = self._add_timezone(converted_datetime, server=server)
        return self.normalize(converted_datetime, server=server)

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

    def get_current_timestamp(self, date_sep='-', main_sep=' ',
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

        if date_sep is None:
            date_sep = ''
        if main_sep is None:
            main_sep = ''
        if time_sep is None:
            time_sep = ''

        current = self.now(server=server, timezone=timezone)
        return '{year}{date_sep}{month}{date_sep}{day}{main_sep}' \
               '{hour}{time_sep}{minute}{time_sep}{second}'.format(
                year=str(current.year).zfill(4),
                month=str(current.month).zfill(2),
                day=str(current.day).zfill(2),
                hour=str(current.hour).zfill(2),
                minute=str(current.minute).zfill(2),
                second=str(current.second).zfill(2),
                date_sep=date_sep,
                main_sep=main_sep,
                time_sep=time_sep)

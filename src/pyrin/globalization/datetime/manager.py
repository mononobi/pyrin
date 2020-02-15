# -*- coding: utf-8 -*-
"""
datetime manager module.
"""

from datetime import datetime

import pytz

import pyrin.configuration.services as config_services
import pyrin.utils.datetime as datetime_utils

from pyrin.core.context import Manager


class DateTimeManager(Manager):
    """
    datetime manager class.
    """

    def __init__(self, **options):
        """
        initializes an instance of DateTimeManager.
        """

        super().__init__()

        default_timezone_name = config_services.get('globalization',
                                                    'locale',
                                                    'babel_default_timezone')
        self.__current_timezone = pytz.timezone(default_timezone_name)

    def now(self, timezone=None):
        """
        gets the current datetime based on given timezone name.

        :param str timezone: timezone name to get current datetime based on it.
                             if not provided, defaults to application
                             current timezone.

        :rtype: datetime
        """

        if timezone is None:
            timezone = self.get_current_timezone()
        else:
            timezone = pytz.timezone(timezone)

        return datetime.now(timezone)

    def get_current_timezone(self):
        """
        gets the application current timezone.

        :rtype: tzinfo
        """

        return self.__current_timezone

    def get_current_timezone_name(self):
        """
        gets the application current timezone name.

        :rtype: str
        """

        return self.get_current_timezone().zone

    def normalize(self, value):
        """
        normalizes input datetime value using application current
        timezone and returns it.
        input value should already have a timezone info.

        :param datetime value: value to get normalized.

        :rtype: datetime
        """

        return self.get_current_timezone().normalize(value)

    def localize(self, value):
        """
        localizes input datetime with application current timezone.
        input value should not have a timezone info.

        :param datetime value: value to be localized.

        :rtype: datetime
        """

        return self.get_current_timezone().localize(value)

    def _add_timezone_info(self, value):
        """
        adds the application current timezone info into input
        value if it has no timezone info.

        :param datetime value: value to add timezone info into it.

        :rtype: datetime
        """

        localized_value = value
        if value.tzinfo is None:
            localized_value = self.get_current_timezone().localize(value)

        return localized_value

    def to_datetime_string(self, value):
        """
        gets the datetime string representation of input value.
        if the value has no timezone info, it adds the application
        current timezone info into it.
        example: `2015-12-24T22:40:15+01:00`

        :param datetime value: input object to be converted.

        :rtype: str
        """

        localized_value = self._add_timezone_info(value)
        return datetime_utils.to_datetime_string(localized_value)

    def to_date_string(self, value):
        """
        gets the date string representation of input value.
        example: `2015-12-24`

        :param Union[datetime, date] value: input object to be converted.

        :rtype: str
        """

        return datetime_utils.to_date_string(value)

    def to_time_string(self, value):
        """
        gets the time string representation of input value.
        if the value has no timezone info, it adds the application
        current timezone info into it.
        example: `23:40:15`

        :param Union[datetime, time] value: input object to be converted.

        :rtype: str
        """

        localized_value = value
        if isinstance(value, datetime):
            localized_value = self._add_timezone_info(value)
        return datetime_utils.to_time_string(localized_value)

    def to_datetime(self, value):
        """
        converts the input value to it's equivalent python datetime.

        :param str value: string representation of datetime to be converted.

        :rtype: datetime
        """

        converted_datetime = datetime_utils.to_datetime(value)
        return self._add_timezone_info(converted_datetime)

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

        if date_sep is None:
            date_sep = ''
        if main_sep is None:
            main_sep = ''
        if time_sep is None:
            time_sep = ''

        current = self.now(timezone)
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

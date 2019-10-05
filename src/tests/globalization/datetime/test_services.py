# -*- coding: utf-8 -*-
"""
datetime test_services module.
"""

from datetime import datetime

import pytest
import pytz

import pyrin.globalization.datetime.services as datetime_services


def test_now():
    """
    gets current datetime based on application current timezone.
    """

    current = datetime_services.now()
    assert current is not None
    assert current.tzinfo is not None
    assert current.tzinfo.zone == datetime_services.get_current_timezone_name()


def test_get_current_timezone(current_timezone):
    """
    gets the application current timezone.
    """

    assert current_timezone == datetime_services.get_current_timezone()


def test_get_current_timezone_name(current_timezone_name):
    """
    gets the application current timezone name.
    """

    assert current_timezone_name == datetime_services.get_current_timezone_name()


def test_normalize(berlin_datetime):
    """
    normalizes input datetime value using application current timezone.
    """

    datetime_default = datetime_services.normalize(berlin_datetime)

    assert berlin_datetime == datetime_default
    assert berlin_datetime.tzinfo != datetime_default.tzinfo


def test_normalize_without_timezone_info():
    """
    normalizes input datetime which has no timezone info
    using application current timezone.
    it should raise an error.
    """

    value = datetime.now()
    with pytest.raises(ValueError):
        datetime_services.normalize(value)


def test_localize(current_timezone_name):
    """
    localizes input datetime with application current timezone.
    """

    datetime_naive = datetime(2019, 10, 2, 18, 0, 0)
    datetime_localized = datetime_services.localize(datetime_naive)

    assert datetime_localized.tzinfo.zone == current_timezone_name


def test_localize_with_timezone_info(berlin_datetime):
    """
    localizes input datetime which already has a timezone
    info with application current timezone.
    it should raise an error.
    """

    timezone_berlin = pytz.timezone('Europe/Berlin')

    with pytest.raises(ValueError):
        timezone_berlin.localize(berlin_datetime)


def test_to_datetime_string(berlin_datetime):
    """
    gets the datetime string representation of input value.
    """

    datetime_string = datetime_services.to_datetime_string(berlin_datetime)

    # we check for UTC offset in both halves of the year to prevent
    # the test failure on different times of year.
    assert datetime_string in ('2019-10-02T18:00:00+02:00', '2019-10-02T18:00:00+01:00')


def test_to_date_string_with_datetime(berlin_datetime):
    """
    gets the date string representation of input datetime.
    """

    date_string = datetime_services.to_date_string(berlin_datetime)

    assert date_string == '2019-10-02'


def test_to_date_string_with_date(berlin_datetime):
    """
    gets the date string representation of input date.
    """

    date_string = datetime_services.to_date_string(berlin_datetime.date())

    assert date_string == '2019-10-02'


def test_to_time_string_wih_datetime(berlin_datetime):
    """
    gets the time string representation of input datetime.
    example: `23:40:15`

    :rtype: str
    """

    time_berlin = datetime_services.to_time_string(berlin_datetime)

    assert time_berlin == '18:00:00'


def test_to_time_string_wih_time(berlin_datetime):
    """
    gets the time string representation of input time.
    example: `23:40:15`

    :rtype: str
    """

    time_berlin = datetime_services.to_time_string(berlin_datetime.timetz())

    assert time_berlin == '18:00:00'


def test_to_datetime_with_timezone():
    """
    converts the input value to it's equivalent python datetime.
    """

    datetime_string = '2019-10-02T18:00:00+02:00'
    datetime_object = datetime_services.to_datetime(datetime_string)

    assert datetime_object is not None
    assert datetime_object.tzinfo is not None
    assert datetime_object.year == 2019 and datetime_object.month == 10 and \
        datetime_object.day == 2 and datetime_object.hour == 18


def test_to_datetime_without_timezone(current_timezone_name):
    """
    converts the input value to it's equivalent python datetime.
    it should add the application current timezone into the result.
    """

    datetime_string = '2019-10-02T18:00:00'
    datetime_object = datetime_services.to_datetime(datetime_string)

    assert datetime_object is not None
    assert datetime_object.tzinfo is not None
    assert datetime_object.tzinfo.zone == current_timezone_name
    assert datetime_object.year == 2019 and datetime_object.month == 10 and \
        datetime_object.day == 2 and datetime_object.hour == 18


def test_to_date():
    """
    converts the input value to it's equivalent python date.
    """

    date_string = '2019-10-02'
    date_object = datetime_services.to_date(date_string)

    assert date_object is not None
    assert date_object.year == 2019 and date_object.month == 10 and \
        date_object.day == 2


def test_to_time_with_timezone():
    """
    converts the input value to it's equivalent python time.
    """

    time_string = '18:10:22+01:00'
    time_object = datetime_services.to_time(time_string)

    assert time_object is not None
    assert time_object.tzinfo is not None
    assert time_object.hour == 18 and time_object.minute == 10 and time_object.second == 22


def test_to_time_without_timezone():
    """
    converts the input value to it's equivalent python time.
    """

    time_string = '18:10:22'
    time_object = datetime_services.to_time(time_string)

    assert time_object is not None
    assert time_object.tzinfo is None
    assert time_object.hour == 18 and time_object.minute == 10 and time_object.second == 22

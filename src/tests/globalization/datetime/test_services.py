# -*- coding: utf-8 -*-
"""
datetime test_services module.
"""

from datetime import datetime

import pytest
import pytz

import pyrin.globalization.datetime.services as datetime_services
import pyrin.configuration.services as config_services


def test_now():
    """
    gets current datetime based on application current timezone.
    """

    current = datetime_services.now()
    assert current is not None
    assert current.tzinfo is not None
    assert current.tzinfo.zone == datetime_services.get_current_timezone_name()


def test_get_current_timezone():
    """
    gets the application current timezone.
    """

    default_timezone_name = config_services.get('globalization',
                                                'datetime',
                                                'default_timezone')

    timezone = pytz.timezone(default_timezone_name)
    assert timezone == datetime_services.get_current_timezone()


def test_get_current_timezone_name():
    """
    gets the application current timezone name.
    """

    default_timezone_name = config_services.get('globalization',
                                                'datetime',
                                                'default_timezone')

    assert default_timezone_name == datetime_services.get_current_timezone_name()


def test_normalize():
    """
    normalizes input datetime value using application current timezone.
    """

    timezone_berlin = pytz.timezone('Europe/Berlin')
    datetime_naive = datetime(2019, 10, 2, 18, 0, 0)
    datetime_berlin = timezone_berlin.localize(datetime_naive)
    datetime_default = datetime_services.normalize(datetime_berlin)

    assert datetime_berlin == datetime_default
    assert datetime_berlin.tzinfo != datetime_default.tzinfo


def test_normalize_without_timezone_info():
    """
    normalizes input datetime which has no timezone info
    using application current timezone.
    it should raise an error.
    """

    value = datetime.now()
    with pytest.raises(ValueError):
        datetime_services.normalize(value)


def test_localize():
    """
    localizes input datetime with application current timezone.
    """

    datetime_naive = datetime(2019, 10, 2, 18, 0, 0)
    datetime_localized = datetime_services.localize(datetime_naive)

    assert datetime_localized.tzinfo.zone == datetime_services.get_current_timezone_name()


def test_localize_with_timezone_info():
    """
    localizes input datetime which already has a timezone
    info with application current timezone.
    it should raise an error.
    """

    timezone_berlin = pytz.timezone('Europe/Berlin')
    datetime_naive = datetime(2019, 10, 2, 18, 0, 0)
    datetime_berlin = timezone_berlin.localize(datetime_naive)

    with pytest.raises(ValueError):
        timezone_berlin.localize(datetime_berlin)


def test_to_datetime_string():
    """
    gets the datetime string representation of input value.
    """

    timezone_berlin = pytz.timezone('Europe/Berlin')
    datetime_naive = datetime(2019, 10, 2, 18, 0, 0)
    datetime_berlin = timezone_berlin.localize(datetime_naive)
    datetime_string = datetime_services.to_datetime_string(datetime_berlin)

    # we check for UTC offset in both halves of the year to prevent
    # the test failure on different times of year.
    assert datetime_string in ('2019-10-02T18:00:00+02:00', '2019-10-02T18:00:00+01:00')


def test_to_date_string_with_datetime():
    """
    gets the date string representation of input datetime.
    """

    timezone_berlin = pytz.timezone('Europe/Berlin')
    datetime_naive = datetime(2019, 10, 2, 18, 0, 0)
    datetime_berlin = timezone_berlin.localize(datetime_naive)
    date_string = datetime_services.to_date_string(datetime_berlin)

    assert date_string == '2019-10-02'


def test_to_date_string_with_date():
    """
    gets the date string representation of input date.
    """

    timezone_berlin = pytz.timezone('Europe/Berlin')
    datetime_naive = datetime(2019, 10, 2, 18, 0, 0)
    datetime_berlin = timezone_berlin.localize(datetime_naive)
    date_string = datetime_services.to_date_string(datetime_berlin.date())

    assert date_string == '2019-10-02'

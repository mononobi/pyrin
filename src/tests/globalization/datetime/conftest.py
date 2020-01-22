# -*- coding: utf-8 -*-
"""
datetime conftest module.
"""

from datetime import datetime

import pytest
import pytz

import pyrin.configuration.services as config_services


@pytest.fixture(scope='function')
def current_timezone_name():
    """
    gets the application current timezone name.

    :rtype: str
    """

    return config_services.get('globalization', 'locale', 'babel_default_timezone')


@pytest.fixture(scope='function')
def current_timezone():
    """
    gets the application current timezone.

    :rtype: tzinfo
    """

    current_tz_name = config_services.get('globalization', 'locale', 'babel_default_timezone')
    return pytz.timezone(current_tz_name)


@pytest.fixture(scope='function')
def berlin_datetime():
    """
    gets a sample Berlin datetime with timezone info.

    :rtype: datetime
    """

    timezone_berlin = pytz.timezone('Europe/Berlin')
    datetime_naive = datetime(2019, 10, 2, 18, 0, 0)
    datetime_berlin = timezone_berlin.localize(datetime_naive)

    return datetime_berlin

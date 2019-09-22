# -*- coding: utf-8 -*-
"""
datetime test_services module.
"""

import pytest

import pyrin.globalization.datetime.services as datetime_services
import pyrin.configuration.services as config_services


def test_now():
    """
    gets current datetime based on application current timezone.
    """

    return datetime_services.now()


def test_get_normalized_datetime():
    """
    normalizes the input value to application default timezone.

    :rtype: datetime
    """


def test_get_current_timezone():
    """
    gets the application current timezone.

    :rtype: tzinfo
    """

    default_timezone = config_services.get('globalization', 'datetime', 'default_timezone')
    assert default_timezone == datetime_services.get_current_timezone().zone

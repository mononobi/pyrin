# -*- coding: utf-8 -*-
"""
localization test_services module.
"""

import pytest

import pyrin.localization.services as locale_services
import pyrin.configuration.services as config_services

from pyrin.localization.exceptions import InvalidLocaleSelectorTypeError, \
    LocaleSelectorHasBeenAlreadySetError, InvalidTimezoneSelectorTypeError, \
    TimezoneSelectorHasBeenAlreadySetError


def test_set_locale_selector_invalid_type():
    """
    sets the given function as locale selector which has an invalid type.
    it should raise an error.
    """

    with pytest.raises(InvalidLocaleSelectorTypeError):
        locale_services.set_locale_selector(None)


def test_set_locale_selector_already_set():
    """
    sets the given function as locale selector which has been already set.
    it should raise an error.
    """

    with pytest.raises(LocaleSelectorHasBeenAlreadySetError):
        locale_services.set_locale_selector(locale_services.get_current_locale)


def test_set_timezone_selector_invalid_type():
    """
    sets the given function as timezone selector which has an invalid type.
    it should raise an error.
    """

    with pytest.raises(InvalidTimezoneSelectorTypeError):
        locale_services.set_timezone_selector(23)


def test_set_timezone_selector_already_set():
    """
    sets the given function as timezone selector which has been already set.
    it should raise an error.
    """

    with pytest.raises(TimezoneSelectorHasBeenAlreadySetError):
        locale_services.set_timezone_selector(locale_services.get_current_timezone)


def test_get_current_locale():
    """
    gets the current locale that should be used for current request.
    it should be the default locale, because there is no request.
    """

    locale = locale_services.get_current_locale()
    default_locale = config_services.get('localization', 'general',
                                         'babel_default_locale')

    assert locale == default_locale


def test_get_current_timezone():
    """
    gets the current timezone that should be used for current request.
    it should be the default timezone, because there is no request.
    """

    timezone = locale_services.get_current_timezone()
    default_timezone = config_services.get('localization', 'general',
                                           'babel_default_timezone')

    assert timezone == default_timezone

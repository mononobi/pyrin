# -*- coding: utf-8 -*-
"""
locale test_services module.
"""

import pytest

import pyrin.globalization.locale.services as locale_services
import pyrin.configuration.services as config_services

from pyrin.globalization.locale.exceptions import InvalidLocaleSelectorTypeError, \
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
    default_locale = config_services.get('globalization', 'locale',
                                         'babel_default_locale')

    assert locale == default_locale


def test_get_current_timezone():
    """
    gets the current timezone that should be used for current request.
    it should be the default timezone, because there is no request.
    """

    timezone = locale_services.get_current_timezone()
    default_timezone = config_services.get('globalization', 'timezone',
                                           'babel_default_timezone')

    assert timezone == default_timezone


def test_locale_exists_valid():
    """
    gets a value indicating that a locale with the given name exists.
    """

    assert locale_services.locale_exists('fa') is True
    assert locale_services.locale_exists('fA') is True
    assert locale_services.locale_exists('en') is True
    assert locale_services.locale_exists('FR') is True


def test_locale_exists_invalid():
    """
    gets a value indicating that a locale with the given name does not exist.
    """

    assert locale_services.locale_exists('11') is not True
    assert locale_services.locale_exists('fake') is not True
    assert locale_services.locale_exists('fa.ir') is not True
    assert locale_services.locale_exists('') is not True
    assert locale_services.locale_exists(' ') is not True
    assert locale_services.locale_exists(None) is not True

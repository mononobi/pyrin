# -*- coding: utf-8 -*-
"""
locale manager module.
"""

from flask_babel import Babel
from babel import localedata

import pyrin.security.session.services as session_services
import pyrin.configuration.services as config_services
import pyrin.globalization.datetime.services as datetime_services

from pyrin.core.structs import Manager
from pyrin.application.services import get_current_app
from pyrin.globalization.locale import LocalePackage
from pyrin.globalization.locale.exceptions import InvalidLocaleSelectorTypeError, \
    InvalidTimezoneSelectorTypeError, LocaleSelectorHasBeenAlreadySetError, \
    TimezoneSelectorHasBeenAlreadySetError


class LocaleManager(Manager):
    """
    locale manager class.
    """

    package_class = LocalePackage

    def __init__(self, **options):
        """
        initializes an instance of LocaleManager.
        """

        super().__init__()

        self._babel = Babel(get_current_app())
        self._default_locale = config_services.get('globalization', 'locale',
                                                   'babel_default_locale')

    def set_locale_selector(self, func):
        """
        sets the given function as locale selector.

        :param function func: function to be set as locale selector.

        :raises InvalidLocaleSelectorTypeError: invalid locale selector type error.

        :raises LocaleSelectorHasBeenAlreadySetError: locale selector has been
                                                      already set error.
        """

        if not callable(func):
            raise InvalidLocaleSelectorTypeError('Input parameter [{locale}] '
                                                 'is not callable.'
                                                 .format(locale=func))

        if self._babel.locale_selector_func is not None:
            raise LocaleSelectorHasBeenAlreadySetError('Locale selector has been already '
                                                       'set and could not be overwritten.')

        self._babel.locale_selector_func = func

    def set_timezone_selector(self, func):
        """
        sets the given function as timezone selector.

        :param function func: function to be set as timezone selector.

        :raises InvalidTimezoneSelectorTypeError: invalid timezone selector type error.

        :raises TimezoneSelectorHasBeenAlreadySetError: timezone selector has been
                                                        already set error.
        """

        if not callable(func):
            raise InvalidTimezoneSelectorTypeError('Input parameter [{timezone}] '
                                                   'is not callable.'
                                                   .format(timezone=func))

        if self._babel.timezone_selector_func is not None:
            raise TimezoneSelectorHasBeenAlreadySetError('Timezone selector has been already '
                                                         'set and could not be overwritten.')

        self._babel.timezone_selector_func = func

    def get_default_locale(self):
        """
        gets the default locale of application from `globalization` config store.

        :rtype: str
        """

        return self._default_locale

    def get_current_locale(self):
        """
        gets the current locale that should be used for current request.

        it never raises an error and returns the default locale if anything goes wrong.

        :rtype: str
        """

        request = session_services.get_safe_current_request()
        locale = None
        if request is not None:
            locale = request.locale

        return locale or self._default_locale

    def get_current_timezone(self):
        """
        gets the current timezone that should be used for current request.

        it never raises an error and returns the default timezone if anything goes wrong.

        :rtype: str
        """

        return datetime_services.get_timezone_name(server=False)

    def locale_exists(self, locale_name):
        """
        gets a value indicating that a locale with the given name exists.

        :param str locale_name: locale name to check for existence.

        :rtype: bool
        """

        return localedata.exists(locale_name)

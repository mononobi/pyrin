# -*- coding: utf-8 -*-
"""
localization manager module.
"""

from flask_babel import Babel

import pyrin.security.session.services as session_services
import pyrin.configuration.services as config_services

from pyrin.core.context import CoreObject
from pyrin.application.services import get_current_app
from pyrin.localization.exceptions import InvalidLocaleSelectorTypeError, \
    InvalidTimezoneSelectorTypeError, LocaleSelectorHasBeenAlreadySetError, \
    TimezoneSelectorHasBeenAlreadySetError


class LocalizationManager(CoreObject):
    """
    localization manager class.
    """

    def __init__(self, **options):
        """
        initializes an instance of LocalizationManager.
        """

        CoreObject.__init__(self)

        self._babel = Babel(get_current_app(), configure_jinja=False)

    def set_locale_selector(self, func):
        """
        sets the given function as locale selector.

        :param callable func: function to be set as locale selector.

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

        :param callable func: function to be set as timezone selector.

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

    def get_current_locale(self):
        """
        gets the current locale that should be used for current request.

        :rtype: str
        """

        current_locale = session_services.get_current_request_context().get('locale', None)
        if current_locale is None:
            current_locale = config_services.get('localization', 'general',
                                                 'babel_default_locale')

        return current_locale

    def get_current_timezone(self):
        """
        gets the current timezone that should be used for current request.

        :rtype: str
        """

        current_timezone = session_services.get_current_request_context().get('timezone', None)
        if current_timezone is None:
            current_timezone = config_services.get('localization', 'general',
                                                   'babel_default_timezone')

        return current_timezone

# -*- coding: utf-8 -*-
"""
localization decorators module.
"""

import pyrin.localization.services as localization_services


def locale_selector():
    """
    decorator to register a locale selector for application.

    :raises InvalidLocaleSelectorTypeError: invalid locale selector type error.

    :raises LocaleSelectorHasBeenAlreadySetError: locale selector has been
                                                  already set error.

    :rtype: callable
    """

    def decorator(func):
        """
        decorates the given function and registers it as locale selector.

        :param callable func: function to register it as locale selector.

        :rtype: callable
        """

        localization_services.set_locale_selector(func)

        return func

    return decorator


def timezone_selector():
    """
    decorator to register a timezone selector for application.

    :raises InvalidTimezoneSelectorTypeError: invalid timezone selector type error.

    :raises TimezoneSelectorHasBeenAlreadySetError: timezone selector has been
                                                    already set error.

    :rtype: callable
    """

    def decorator(func):
        """
        decorates the given function and registers it as timezone selector.

        :param callable func: function to register it as timezone selector.

        :rtype: callable
        """

        localization_services.set_timezone_selector(func)

        return func

    return decorator

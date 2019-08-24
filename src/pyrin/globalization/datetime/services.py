# -*- coding: utf-8 -*-
"""
datetime services module.
"""

from pyrin.application.services import get_component
from pyrin.globalization.datetime import DateTimePackage


def set_locale_selector(func):
    """
    sets the given function as locale selector.

    :param callable func: function to be set as locale selector.

    :raises InvalidLocaleSelectorTypeError: invalid locale selector type error.

    :raises LocaleSelectorHasBeenAlreadySetError: locale selector has been
                                                  already set error.
    """

    get_component(DateTimePackage.COMPONENT_NAME).set_locale_selector(func)

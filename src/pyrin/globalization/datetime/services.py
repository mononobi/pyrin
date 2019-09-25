# -*- coding: utf-8 -*-
"""
datetime services module.
"""

from pyrin.application.services import get_component
from pyrin.globalization.datetime import DateTimePackage


def now():
    """
    gets current datetime based on application current timezone.

    :rtype: datetime
    """

    return get_component(DateTimePackage.COMPONENT_NAME).now()


def get_current_timezone():
    """
    gets the application current timezone.

    :rtype: tzinfo
    """

    return get_component(DateTimePackage.COMPONENT_NAME).get_current_timezone()

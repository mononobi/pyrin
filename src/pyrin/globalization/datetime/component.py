# -*- coding: utf-8 -*-
"""
datetime component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.globalization.datetime import DateTimePackage
from pyrin.globalization.datetime.manager import DateTimeManager


@component(DateTimePackage.COMPONENT_NAME)
class DateTimeComponent(Component, DateTimeManager):
    """
    datetime component class.
    """
    pass

# -*- coding: utf-8 -*-
"""
range component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.utilities.range import UtilitiesRangePackage
from pyrin.utilities.range.manager import RangeManager


@component(UtilitiesRangePackage.COMPONENT_NAME)
class RangeComponent(Component, RangeManager):
    """
    range component class.
    """
    pass

# -*- coding: utf-8 -*-
"""
filtering component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.filtering import FilteringPackage
from pyrin.filtering.manager import FilteringManager


@component(FilteringPackage.COMPONENT_NAME)
class FilteringComponent(Component, FilteringManager):
    """
    filtering component class.
    """
    pass

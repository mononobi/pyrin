# -*- coding: utf-8 -*-
"""
caching component module.
"""

from pyrin.application.decorators import component
from pyrin.caching import CachingPackage
from pyrin.caching.manager import CachingManager
from pyrin.application.structs import Component


@component(CachingPackage.COMPONENT_NAME)
class CachingComponent(Component, CachingManager):
    """
    caching component class.
    """
    pass

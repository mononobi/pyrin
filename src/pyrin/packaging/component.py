# -*- coding: utf-8 -*-
"""
packaging component module.
"""

from pyrin.context import Component
from pyrin.packaging.manager import PackagingManager
from pyrin.settings.static import DEFAULT_COMPONENT_KEY


class PackagingComponent(Component, PackagingManager):
    """
    packaging component class.
    """

    COMPONENT_ID = (__name__, DEFAULT_COMPONENT_KEY)

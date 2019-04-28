# -*- coding: utf-8 -*-
"""
packaging component module.
"""

from bshop.core.context import Component
from bshop.core.packaging.manager import PackagingManager


class PackagingComponent(Component, PackagingManager):
    """
    packaging component class.
    """

    COMPONENT_ID = __name__

# -*- coding: utf-8 -*-
"""
packaging component module.
"""

from pyrin.core.context import Component
from pyrin.packaging.manager import PackagingManager


class PackagingComponent(Component, PackagingManager):
    """
    packaging component class.
    """

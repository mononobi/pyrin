# -*- coding: utf-8 -*-
"""
packaging component module.
"""

from pyrin.application.structs import Component
from pyrin.packaging.manager import PackagingManager


class PackagingComponent(Component, PackagingManager):
    """
    packaging component class.

    an instance of this class will be registered into application components
    on startup, and we shouldn't use `@component` decorator for this class.
    """
    pass

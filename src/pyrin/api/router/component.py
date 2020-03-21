# -*- coding: utf-8 -*-
"""
router component module.
"""

from pyrin.api.router import RouterPackage
from pyrin.api.router.manager import RouterManager
from pyrin.application.structs import Component
from pyrin.application.decorators import component


@component(RouterPackage.COMPONENT_NAME)
class RouterComponent(Component, RouterManager):
    """
    router component class.
    """
    pass

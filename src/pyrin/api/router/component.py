# -*- coding: utf-8 -*-
"""
router component module.
"""

from pyrin.api.router.manager import RouterManager
from pyrin.application.decorators import component
from pyrin.context import Component
from pyrin.settings.static import DEFAULT_COMPONENT_KEY


@component()
class RouterComponent(Component, RouterManager):
    """
    router component class.
    """

    COMPONENT_ID = (__name__, DEFAULT_COMPONENT_KEY)

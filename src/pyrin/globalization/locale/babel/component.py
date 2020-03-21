# -*- coding: utf-8 -*-
"""
babel component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.globalization.locale.babel import BabelPackage
from pyrin.globalization.locale.babel.manager import BabelManager


@component(BabelPackage.COMPONENT_NAME)
class BabelComponent(Component, BabelManager):
    """
    babel component class.
    """
    pass

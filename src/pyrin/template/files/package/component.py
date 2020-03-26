# -*- coding: utf-8 -*-
"""
PACKAGE_NAME component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component

from PACKAGE_FULL_NAME import PACKAGE_CLASS_NAMEPackage
from PACKAGE_FULL_NAME.manager import PACKAGE_CLASS_NAMEManager


@component(PACKAGE_CLASS_NAMEPackage.COMPONENT_NAME)
class PACKAGE_CLASS_NAMEComponent(Component, PACKAGE_CLASS_NAMEManager):
    """
    PACKAGE_NAME component class.
    """
    pass

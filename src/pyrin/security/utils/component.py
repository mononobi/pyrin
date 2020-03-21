# -*- coding: utf-8 -*-
"""
security utils component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.security.utils import SecurityUtilsPackage
from pyrin.security.utils.manager import SecurityUtilsManager


@component(SecurityUtilsPackage.COMPONENT_NAME)
class SecurityUtilsComponent(Component, SecurityUtilsManager):
    """
    security utils component class.
    """
    pass

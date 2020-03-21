# -*- coding: utf-8 -*-
"""
security component module.
"""

from pyrin.application.decorators import component
from pyrin.security import SecurityPackage
from pyrin.security.manager import SecurityManager
from pyrin.application.structs import Component


@component(SecurityPackage.COMPONENT_NAME)
class SecurityComponent(Component, SecurityManager):
    """
    security component class.
    """
    pass

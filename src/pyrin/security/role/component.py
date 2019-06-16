# -*- coding: utf-8 -*-
"""
role component module.
"""

from pyrin.application.decorators import component
from pyrin.security.role import RolePackage
from pyrin.security.role.manager import RoleManager
from pyrin.application.context import Component


@component(RolePackage.COMPONENT_NAME)
class RoleComponent(Component, RoleManager):
    """
    role component class.
    """

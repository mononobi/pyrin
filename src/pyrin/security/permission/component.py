# -*- coding: utf-8 -*-
"""
permission component module.
"""

from pyrin.application.decorators import component
from pyrin.security.permission import PermissionPackage
from pyrin.security.permission.manager import PermissionManager
from pyrin.application.structs import Component


@component(PermissionPackage.COMPONENT_NAME)
class PermissionComponent(Component, PermissionManager):
    """
    permission component class.
    """
    pass

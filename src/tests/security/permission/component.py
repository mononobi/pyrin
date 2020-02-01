# -*- coding: utf-8 -*-
"""
permission component module.
"""

from pyrin.application.decorators import component
from pyrin.application.context import Component

from tests.security.permission import PermissionPackage
from tests.security.permission.manager import PermissionManager


@component(PermissionPackage.COMPONENT_NAME, replace=True)
class PermissionComponent(Component, PermissionManager):
    """
    permission component class.
    """
    pass

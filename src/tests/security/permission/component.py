# -*- coding: utf-8 -*-
"""
permission component module.
"""

from pyrin.application.decorators import component
from pyrin.application.context import Component

from tests.security.permission import TestPermissionPackage
from tests.security.permission.manager import TestPermissionManager


@component(TestPermissionPackage.COMPONENT_NAME, replace=True)
class TestPermissionComponent(Component, TestPermissionManager):
    """
    test permission component class.
    """

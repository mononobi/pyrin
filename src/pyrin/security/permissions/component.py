# -*- coding: utf-8 -*-
"""
permissions component module.
"""

from pyrin.application.decorators import component
from pyrin.security.permissions import PermissionsPackage
from pyrin.security.permissions.manager import PermissionsManager
from pyrin.application.context import Component


@component(PermissionsPackage.COMPONENT_NAME)
class PermissionsComponent(Component, PermissionsManager):
    """
    permissions component class.
    """

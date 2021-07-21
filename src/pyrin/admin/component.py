# -*- coding: utf-8 -*-
"""
admin component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.admin import AdminPackage
from pyrin.admin.manager import AdminManager


@component(AdminPackage.COMPONENT_NAME)
class AdminComponent(Component, AdminManager):
    """
    admin component class.
    """
    pass

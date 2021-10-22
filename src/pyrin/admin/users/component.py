# -*- coding: utf-8 -*-
"""
admin users component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.admin.users import AdminUsersPackage
from pyrin.admin.users.manager import AdminUsersManager


@component(AdminUsersPackage.COMPONENT_NAME)
class AdminUsersComponent(Component, AdminUsersManager):
    """
    admin users component class.
    """
    pass

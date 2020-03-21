# -*- coding: utf-8 -*-
"""
users component module.
"""

from pyrin.application.decorators import component
from pyrin.security.users import UsersPackage
from pyrin.security.users.manager import UsersManager
from pyrin.application.structs import Component


@component(UsersPackage.COMPONENT_NAME)
class UsersComponent(Component, UsersManager):
    """
    users component class.
    """
    pass

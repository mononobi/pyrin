# -*- coding: utf-8 -*-
"""
users internal component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.users.internal import InternalUsersPackage
from pyrin.users.internal.manager import InternalUsersManager


@component(InternalUsersPackage.COMPONENT_NAME)
class InternalUsersComponent(Component, InternalUsersManager):
    """
    internal users component class.
    """
    pass

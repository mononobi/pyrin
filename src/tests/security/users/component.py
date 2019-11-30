# -*- coding: utf-8 -*-
"""
users component module.
"""

from pyrin.application.decorators import component
from pyrin.application.context import Component

from tests.security.users import TestUsersPackage
from tests.security.users.manager import TestUsersManager


@component(TestUsersPackage.COMPONENT_NAME, replace=True)
class TestUsersComponent(Component, TestUsersManager):
    """
    test users component class.
    """

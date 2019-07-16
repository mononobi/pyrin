# -*- coding: utf-8 -*-
"""
security component module.
"""

from pyrin.application.decorators import component
from pyrin.application.context import Component

from tests.security import TestSecurityPackage
from tests.security.manager import TestSecurityManager


@component(TestSecurityPackage.COMPONENT_NAME, replace=True)
class TestSecurityComponent(Component, TestSecurityManager):
    """
    test security component class.
    """

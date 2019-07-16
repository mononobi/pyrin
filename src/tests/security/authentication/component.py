# -*- coding: utf-8 -*-
"""
authentication component module.
"""

from pyrin.application.decorators import component
from pyrin.application.context import Component

from tests.security.authentication import TestAuthenticationPackage
from tests.security.authentication.manager import TestAuthenticationManager


@component(TestAuthenticationPackage.COMPONENT_NAME, replace=True)
class TestAuthenticationComponent(Component, TestAuthenticationManager):
    """
    test authentication component class.
    """

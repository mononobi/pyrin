# -*- coding: utf-8 -*-
"""
session component module.
"""

from pyrin.application.decorators import component
from pyrin.application.context import Component

from tests.security.session import TestSessionPackage
from tests.security.session.manager import TestSessionManager


@component(TestSessionPackage.COMPONENT_NAME, replace=True)
class TestSessionComponent(Component, TestSessionManager):
    """
    test session component class.
    """

# -*- coding: utf-8 -*-
"""
authentication component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component

from tests.unit.security.authentication import AuthenticationPackage
from tests.unit.security.authentication.manager import AuthenticationManager


@component(AuthenticationPackage.COMPONENT_NAME, replace=True)
class AuthenticationComponent(Component, AuthenticationManager):
    """
    authentication component class.
    """
    pass

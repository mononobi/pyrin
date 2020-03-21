# -*- coding: utf-8 -*-
"""
authentication component module.
"""

from pyrin.application.decorators import component
from pyrin.security.authentication import AuthenticationPackage
from pyrin.security.authentication.manager import AuthenticationManager
from pyrin.application.structs import Component


@component(AuthenticationPackage.COMPONENT_NAME)
class AuthenticationComponent(Component, AuthenticationManager):
    """
    authentication component class.
    """
    pass

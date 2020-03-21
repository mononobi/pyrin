# -*- coding: utf-8 -*-
"""
authorization component module.
"""

from pyrin.application.decorators import component
from pyrin.security.authorization import AuthorizationPackage
from pyrin.security.authorization.manager import AuthorizationManager
from pyrin.application.structs import Component


@component(AuthorizationPackage.COMPONENT_NAME)
class AuthorizationComponent(Component, AuthorizationManager):
    """
    authorization component class.
    """
    pass

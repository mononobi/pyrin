# -*- coding: utf-8 -*-
"""
token component module.
"""

from pyrin.application.decorators import component
from pyrin.security.token import TokenPackage
from pyrin.security.token.manager import TokenManager
from pyrin.application.structs import Component


@component(TokenPackage.COMPONENT_NAME)
class TokenComponent(Component, TokenManager):
    """
    token component class.
    """
    pass

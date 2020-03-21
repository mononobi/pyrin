# -*- coding: utf-8 -*-
"""
session component module.
"""

from pyrin.application.decorators import component
from pyrin.security.session import SessionPackage
from pyrin.security.session.manager import SessionManager
from pyrin.application.structs import Component


@component(SessionPackage.COMPONENT_NAME)
class SessionComponent(Component, SessionManager):
    """
    session component class.
    """
    pass

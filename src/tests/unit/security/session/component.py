# -*- coding: utf-8 -*-
"""
session component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component

from tests.unit.security.session import SessionPackage
from tests.unit.security.session.manager import SessionManager


@component(SessionPackage.COMPONENT_NAME, replace=True)
class SessionComponent(Component, SessionManager):
    """
    session component class.
    """
    pass

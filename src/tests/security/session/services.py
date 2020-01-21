# -*- coding: utf-8 -*-
"""
session services module.
"""

from pyrin.application.services import get_component

from tests.security.session import SessionPackage


def inject_new_request():
    """
    injects a new request into current request object.
    """

    get_component(SessionPackage.COMPONENT_NAME).inject_new_request()


def clear_current_request():
    """
    clears current request object.
    """

    get_component(SessionPackage.COMPONENT_NAME).clear_current_request()

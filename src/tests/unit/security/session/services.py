# -*- coding: utf-8 -*-
"""
session services module.
"""

from pyrin.application.services import get_component

from tests.unit.security.session import SessionPackage


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


def set_access_token(token):
    """
    sets the given access token in current request.

    :param str token: access token.
    """

    get_component(SessionPackage.COMPONENT_NAME).set_access_token(token)


def set_refresh_token(token):
    """
    sets the given refresh token in current request.

    :param str token: refresh token.
    """

    get_component(SessionPackage.COMPONENT_NAME).set_refresh_token(token)

# -*- coding: utf-8 -*-
"""
authentication services module.
"""

from pyrin.application.services import get_component
from pyrin.security.authentication import AuthenticationPackage


def authenticate(token, **options):
    """
    authenticates given token and pushes the authenticated data into request context.
    if authentication fails, authenticated data will not be pushed into request context.

    :param str token: token to be authenticated.

    :raises AuthenticationFailedError: authentication failed error.
    """

    return get_component(AuthenticationPackage.COMPONENT_NAME).authenticate(token, **options)

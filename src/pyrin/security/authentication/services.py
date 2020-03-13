# -*- coding: utf-8 -*-
"""
authentication services module.
"""

from pyrin.application.services import get_component
from pyrin.security.authentication import AuthenticationPackage


def authenticate(client_request, **options):
    """
    authenticates given request and pushes the authenticated data into request context.

    if authentication fails, authenticated data will not be pushed into request context.

    :param CoreRequest client_request: request to be authenticated.

    :raises AuthenticationFailedError: authentication failed error.
    :raises InvalidPayloadDataError: invalid payload data error.
    :raises AccessTokenRequiredError: access token required error.
    """

    return get_component(AuthenticationPackage.COMPONENT_NAME).authenticate(client_request,
                                                                            **options)

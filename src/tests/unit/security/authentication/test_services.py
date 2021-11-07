# -*- coding: utf-8 -*-
"""
authentication test_services module.
"""

import pytest

import pyrin.security.authentication.services as authentication_services
import pyrin.security.session.services as session_services

from pyrin.security.exceptions import AuthenticationFailedError
from pyrin.security.authentication.handlers.exceptions import AccessTokenRequiredError, \
    InvalidAccessTokenError


def test_authenticate_with_fresh_access_token(client_request_fresh_access_token):
    """
    authenticates given request with fresh access token and
    pushes the authenticated data into request context.
    """

    authentication_services.authenticate(client_request_fresh_access_token,
                                         authenticator='test')
    client_request = session_services.get_current_request()
    assert client_request is not None
    assert client_request.user is not None
    assert client_request.user == 100


def test_authenticate_with_access_token(client_request_access_token):
    """
    authenticates given request with access token and
    pushes the authenticated data into request context.
    """

    authentication_services.authenticate(client_request_access_token,
                                         authenticator='test')
    client_request = session_services.get_current_request()
    assert client_request is not None
    assert client_request.user is not None
    assert client_request.user == 200


def test_authenticate_with_refresh_token(client_request_refresh_token):
    """
    authenticates given request with access token.
    it should raise an error.
    """

    with pytest.raises(InvalidAccessTokenError):
        authentication_services.authenticate(client_request_refresh_token,
                                             authenticator='test')


def test_authenticate_without_token(client_request_without_token):
    """
    authenticates given request that has no token.
    it should not push anything into request object.
    """

    with pytest.raises(AccessTokenRequiredError):
        authentication_services.authenticate(client_request_without_token,
                                             authenticator='test')

    client_request = session_services.get_current_request()
    assert client_request is not None
    assert client_request.user is None


def test_authenticate_with_no_identity_token(client_request_no_identity_token):
    """
    authenticates given request with an access token
    which has no user identity in it's payload.
    it should raise an error.
    """

    with pytest.raises(AuthenticationFailedError):
        authentication_services.authenticate(client_request_no_identity_token,
                                             authenticator='test')


def test_authenticate_with_invalid_token(client_request_invalid_token):
    """
    authenticates given request with an invalid token.
    it should raise an error.
    """

    with pytest.raises(AuthenticationFailedError):
        authentication_services.authenticate(client_request_invalid_token,
                                             authenticator='test')

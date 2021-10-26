# -*- coding: utf-8 -*-
"""
authentication test_services module.
"""

import pytest

import pyrin.security.authentication.services as authentication_services
import pyrin.security.session.services as session_services

from pyrin.security.authentication.exceptions import AuthenticationFailedError
from pyrin.security.authentication.handlers.exceptions import AccessTokenRequiredError


def test_authenticate_with_fresh_access_token(client_request_fresh_access_token):
    """
    authenticates given request with fresh access token and
    pushes the authenticated data into request context.
    """

    authentication_services.authenticate(client_request_fresh_access_token)
    client_request = session_services.get_current_request()
    assert client_request is not None
    assert client_request.user is not None
    assert client_request.user.user_id == 100
    assert session_services.is_fresh()
    assert client_request.get_context('token_header') is not None
    assert client_request.get_context('token_payload') is not None


def test_authenticate_with_access_token(client_request_access_token):
    """
    authenticates given request with access token and
    pushes the authenticated data into request context.
    """

    authentication_services.authenticate(client_request_access_token)
    client_request = session_services.get_current_request()
    assert client_request is not None
    assert client_request.user is not None
    assert client_request.user.user_id == 200
    assert not session_services.is_fresh()
    assert client_request.get_context('token_header') is not None
    assert client_request.get_context('token_payload') is not None


def test_authenticate_with_refresh_token(client_request_refresh_token):
    """
    authenticates given request with access token.
    it should raise an error.
    """

    with pytest.raises(AccessTokenRequiredError):
        authentication_services.authenticate(client_request_refresh_token)


def test_authenticate_without_token(client_request_without_token):
    """
    authenticates given request that has no token.
    it should not push anything into request object.
    """

    authentication_services.authenticate(client_request_without_token)
    client_request = session_services.get_current_request()
    assert client_request is not None
    assert client_request.user is None
    assert not session_services.is_fresh()
    assert client_request.get_context('token_header') is None
    assert client_request.get_context('token_payload') is None


def test_authenticate_with_no_identity_token(client_request_no_identity_token):
    """
    authenticates given request with an access token
    which has no user identity in it's payload.
    it should raise an error.
    """

    with pytest.raises(AuthenticationFailedError):
        authentication_services.authenticate(client_request_no_identity_token)


def test_authenticate_with_invalid_token(client_request_invalid_token):
    """
    authenticates given request with an invalid token.
    it should raise an error.
    """

    with pytest.raises(AuthenticationFailedError):
        authentication_services.authenticate(client_request_invalid_token)

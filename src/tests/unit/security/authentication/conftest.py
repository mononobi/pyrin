# -*- coding: utf-8 -*-
"""
authentication conftest module.
"""

import pytest

import pyrin.security.session.services as session_services
import pyrin.security.token.services as token_services

from pyrin.core.structs import DTO

import tests.unit.security.session.services as test_session_services


@pytest.fixture(scope='function')
def client_request_fresh_access_token():
    """
    gets a mock client request object with fresh access token.

    :rtype: CoreRequestMock
    """

    test_session_services.clear_current_request()
    test_session_services.inject_new_request()
    payload = DTO(user_id=100)
    token = token_services.generate_access_token(payload, is_fresh=True)
    session_services.get_current_request().context['authorization'] = token

    return session_services.get_current_request()


@pytest.fixture(scope='function')
def client_request_access_token():
    """
    gets a mock client request object with access token.

    :rtype: CoreRequestMock
    """

    test_session_services.clear_current_request()
    test_session_services.inject_new_request()
    payload = DTO(user_id=200)
    token = token_services.generate_access_token(payload)
    session_services.get_current_request().context['authorization'] = token

    return session_services.get_current_request()


@pytest.fixture(scope='function')
def client_request_refresh_token():
    """
    gets a mock client request object with refresh token.

    :rtype: CoreRequestMock
    """

    test_session_services.clear_current_request()
    test_session_services.inject_new_request()
    payload = DTO(user_id=300)
    token = token_services.generate_refresh_token(payload)
    session_services.get_current_request().context['authorization'] = token

    return session_services.get_current_request()


@pytest.fixture(scope='function')
def client_request_without_token():
    """
    gets a mock client request object without a token.

    :rtype: CoreRequestMock
    """

    test_session_services.clear_current_request()
    test_session_services.inject_new_request()

    return session_services.get_current_request()


@pytest.fixture(scope='function')
def client_request_no_identity_token():
    """
    gets a mock client request object with an access token
    which has no user identity in it's payload.

    :rtype: CoreRequestMock
    """

    test_session_services.clear_current_request()
    test_session_services.inject_new_request()
    payload = DTO()
    token = token_services.generate_access_token(payload)
    session_services.get_current_request().context['authorization'] = token

    return session_services.get_current_request()


@pytest.fixture(scope='function')
def client_request_invalid_token():
    """
    gets a mock client request object with an invalid token.

    :rtype: CoreRequestMock
    """

    test_session_services.clear_current_request()
    test_session_services.inject_new_request()
    session_services.get_current_request().context['authorization'] = 'an invalid token'

    return session_services.get_current_request()

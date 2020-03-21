# -*- coding: utf-8 -*-
"""
authorization conftest module.
"""

import pytest

import pyrin.security.authentication.services as authentication_services
import pyrin.security.session.services as session_services
import pyrin.security.token.services as token_services

from pyrin.core.structs import DTO

import tests.security.session.services as test_session_services


@pytest.fixture(scope='function')
def client_request_unauthenticated():
    """
    gets a mock client request object which is unauthenticated.

    :rtype: CoreRequestMock
    """

    test_session_services.clear_current_request()
    test_session_services.inject_new_request()
    payload = DTO(user_id=400)
    token = token_services.generate_access_token(payload, is_fresh=True)
    session_services.get_current_request().context['authorization'] = token

    return session_services.get_current_request()


@pytest.fixture(scope='function')
def client_request_authenticated():
    """
    gets a mock client request object with authenticated user.

    :rtype: CoreRequestMock
    """

    test_session_services.clear_current_request()
    test_session_services.inject_new_request()
    payload = DTO(user_id=500)
    token = token_services.generate_access_token(payload, is_fresh=True)
    session_services.get_current_request().context['authorization'] = token
    authentication_services.authenticate(session_services.get_current_request())

    return session_services.get_current_request()


@pytest.fixture(scope='function')
def no_client_request():
    """
    resets the client request object.
    """

    test_session_services.clear_current_request()

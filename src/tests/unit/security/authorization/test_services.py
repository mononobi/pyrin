# -*- coding: utf-8 -*-
"""
authorization test_services module.
"""

import pytest

import pyrin.security.authorization.services as authorization_services

from pyrin.core.structs import DTO
from pyrin.security.authorization.exceptions import AuthorizationFailedError, \
    UserNotAuthenticatedError

from tests.unit.security.permissions import PERMISSION_TEST_ONE, PERMISSION_TEST_TWO, \
    PERMISSION_TEST_THREE, PERMISSION_TEST_FOUR, PERMISSION_TEST_FIVE


def test_authorize_invalid_user():
    """
    authorizes the given invalid user for specified permission.
    it should raise an error.
    """

    with pytest.raises(UserNotAuthenticatedError):
        authorization_services.authorize(None, PERMISSION_TEST_ONE)


def test_authorize_single_permission():
    """
    authorizes the given user for specified permission.
    """

    authorization_services.authorize(DTO(user_id=1000), PERMISSION_TEST_ONE)


def test_authorize_multiple_permissions():
    """
    authorizes the given user for specified permissions.
    """

    authorization_services.authorize(DTO(user_id=1000), [PERMISSION_TEST_ONE,
                                                         PERMISSION_TEST_TWO,
                                                         PERMISSION_TEST_THREE])


def test_authorize_unavailable_single_permission():
    """
    authorizes the given user for specified permission which the user does not have.
    it should raise an error.
    """

    with pytest.raises(AuthorizationFailedError):
        authorization_services.authorize(DTO(user_id=1000), PERMISSION_TEST_FOUR)


def test_authorize_unavailable_multiple_permissions():
    """
    authorizes the given user for specified permissions which
    the user does not have any of them.
    it should raise an error.
    """

    with pytest.raises(AuthorizationFailedError):
        authorization_services.authorize(DTO(user_id=1000), [PERMISSION_TEST_FOUR,
                                                             PERMISSION_TEST_FIVE])


def test_authorize_unavailable_mixed_permissions():
    """
    authorizes the given user for specified permissions which
    the user does not have some of them.
    it should raise an error.
    """

    with pytest.raises(AuthorizationFailedError):
        authorization_services.authorize(DTO(user_id=1000), [PERMISSION_TEST_ONE,
                                                             PERMISSION_TEST_FOUR,
                                                             PERMISSION_TEST_TWO,
                                                             PERMISSION_TEST_FIVE])


def test_is_authorized_current_user(client_request_authenticated):
    """
    gets a value indicating that the current user is authorized for given permission.
    """

    authorized = authorization_services.is_authorized(PERMISSION_TEST_ONE)
    assert authorized is True


def test_is_authorized_current_user_unavailable_permissions(client_request_authenticated):
    """
    gets a value indicating that the current user
    is not authorized for given permissions.
    """

    authorized = authorization_services.is_authorized([PERMISSION_TEST_FOUR,
                                                       PERMISSION_TEST_FIVE])
    assert authorized is False


def test_is_authorized_current_user_unavailable_permission(client_request_authenticated):
    """
    gets a value indicating that the current user
    is not authorized for given permission.
    """

    authorized = authorization_services.is_authorized([PERMISSION_TEST_FIVE])
    assert authorized is False


def test_is_authorized_current_user_unauthenticated(client_request_unauthenticated):
    """
    gets a value indicating that the current user is not authorized for given permission.
    the user is not authenticated so it should not be authorized.
    """

    authorized = authorization_services.is_authorized(PERMISSION_TEST_ONE)
    assert authorized is False


def test_is_authorized_current_user_no_request(no_client_request):
    """
    gets a value indicating that the current user is authorized for given permission.
    there is no request so it should raise an error.
    """

    with pytest.raises(AttributeError):
        authorization_services.is_authorized(PERMISSION_TEST_TWO)


def test_is_authorized_single_permission():
    """
    gets a value indicating that specified user is authorized for given permission.
    """

    authorized = authorization_services.is_authorized(PERMISSION_TEST_ONE,
                                                      user=DTO(user_id=1000))

    assert authorized is True


def test_is_authorized_multiple_permissions():
    """
    gets a value indicating that specified user is authorized for given permissions.
    """

    authorized = authorization_services.is_authorized([PERMISSION_TEST_ONE,
                                                       PERMISSION_TEST_TWO,
                                                       PERMISSION_TEST_THREE],
                                                      user=DTO(user_id=1000))

    assert authorized is True

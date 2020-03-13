# -*- coding: utf-8 -*-
"""
router test_services module.
"""

import pytest

import pyrin.api.router.services as router_services

from pyrin.api.router.exceptions import RouteAuthenticationMismatchError
from pyrin.api.router.handlers.protected import FreshProtectedRoute, ProtectedRoute
from pyrin.api.router.handlers.public import PublicRoute
from pyrin.application.exceptions import DuplicateRouteURLError
from pyrin.core.enumerations import HTTPMethodEnum
from pyrin.api.router.handlers.exceptions import MaxContentLengthLimitMismatchError, \
    InvalidViewFunctionTypeError, PermissionTypeError

from tests.security.permission.base import PermissionMock
from tests.common.mock_functions import mock_view_function


def test_create_route_fresh_protected():
    """
    creates the appropriate route based on the input parameters.
    it should create a fresh protected route.
    """

    route = router_services.create_route('/api/router/fresh_protected',
                                         methods=HTTPMethodEnum.GET,
                                         view_function=mock_view_function,
                                         fresh_token=True,
                                         max_content_length=15000)

    assert isinstance(route, FreshProtectedRoute)


def test_create_route_public():
    """
    creates the appropriate route based on the input parameters.
    it should create a public route.
    """

    route = router_services.create_route('/api/router/public',
                                         methods=HTTPMethodEnum.POST,
                                         view_function=mock_view_function,
                                         login_required=False,
                                         max_content_length=12000)

    assert isinstance(route, PublicRoute)


def test_create_route_protected_with_permissions():
    """
    creates the appropriate route based on the input parameters.
    it should create a protected route.
    """

    permissions = []
    permissions.append(PermissionMock(100, 'permission_100'))
    permissions.append(PermissionMock(101, 'permission_101'))

    route = router_services.create_route('/api/router/protected',
                                         methods=HTTPMethodEnum.DELETE,
                                         view_function=mock_view_function,
                                         max_content_length=15000,
                                         permissions=permissions)

    assert isinstance(route, ProtectedRoute)


def test_create_route_fresh_protected_with_single_permission():
    """
    creates the appropriate route based on the input parameters.
    it should create a fresh protected route.
    """

    permission = PermissionMock(102, 'permission_102')
    route = router_services.create_route('/api/router/fresh_protected_with_permission',
                                         methods=HTTPMethodEnum.POST,
                                         view_function=mock_view_function,
                                         max_content_length=500,
                                         fresh_token=True,
                                         permissions=permission)

    assert isinstance(route, FreshProtectedRoute)


def test_create_route_protected_with_invalid_permissions():
    """
    creates the appropriate route based on the input parameters.
    it should raise an error due to invalid permission.
    """

    with pytest.raises(PermissionTypeError):
        permissions = []
        permissions.append(PermissionMock(103, 'permission_103'))
        permissions.append(1)

        route = router_services.create_route('/api/router/invalid_permission',
                                             methods=HTTPMethodEnum.DELETE,
                                             view_function=mock_view_function,
                                             max_content_length=15000,
                                             permissions=permissions)


def test_create_route_with_mismatch_authentication():
    """
    creates the appropriate route based on the input parameters.
    it should raise an error due to mismatch in authentication options.
    """

    with pytest.raises(RouteAuthenticationMismatchError):
        route = router_services.create_route('/api/router/mismatch_protected',
                                             methods=HTTPMethodEnum.GET,
                                             view_function=mock_view_function,
                                             fresh_token=True,
                                             login_required=False,
                                             max_content_length=15000)


def test_create_route_with_invalid_max_content_length():
    """
    creates the appropriate route based on the input parameters.
    it should raise an error due to invalid content length.
    """

    with pytest.raises(MaxContentLengthLimitMismatchError):
        route = router_services.create_route('/api/router/over_max_content_length',
                                             methods=HTTPMethodEnum.GET,
                                             view_function=mock_view_function,
                                             fresh_token=True,
                                             login_required=True,
                                             max_content_length=99999999999999999)


def test_create_route_with_invalid_view_function():
    """
    creates the appropriate route based on the input parameters.
    it should raise an error due to invalid view function.
    """

    with pytest.raises(InvalidViewFunctionTypeError):
        route = router_services.create_route('/api/router/invalid_view_function',
                                             methods=HTTPMethodEnum.PUT,
                                             view_function=1,
                                             fresh_token=False,
                                             login_required=False)


def test_create_route_validate_max_content_length():
    """
    creates the appropriate route based on the input parameters.
    then validates the specified max content length.
    """

    route = router_services.create_route('/api/router/check_max_content',
                                         methods=HTTPMethodEnum.PUT,
                                         view_function=mock_view_function,
                                         fresh_token=False,
                                         login_required=False,
                                         max_content_length=12345)

    assert route.max_content_length == 12345


def test_add_route():
    """
    adds a new protected route in application routes.
    """

    permission = PermissionMock(104, 'permission_104')
    router_services.add_route('/tests/api/router/fake_route',
                              view_func=mock_view_function,
                              methods=HTTPMethodEnum.GET,
                              permissions=permission,
                              login_required=True)


def test_add_route_duplicate():
    """
    adds a new duplicated route in application routes.
    it should raise an error.
    """

    with pytest.raises(DuplicateRouteURLError):
        permission = PermissionMock(105, 'permission_105')
        router_services.add_route('/tests/api/router/duplicate_route',
                                  view_func=mock_view_function,
                                  methods=HTTPMethodEnum.GET,
                                  permissions=permission,
                                  login_required=True)

        router_services.add_route('/tests/api/router/duplicate_route',
                                  view_func=mock_view_function,
                                  methods=HTTPMethodEnum.POST,
                                  login_required=False,
                                  max_content_length=123)


def test_add_route_duplicate_with_replace():
    """
    adds a new duplicated route in application routes with replace option.
    it should not raise an error.
    """

    permissions = []
    permissions.append(PermissionMock(106, 'permission_106'))
    permissions.append(PermissionMock(107, 'permission_107'))
    router_services.add_route('/tests/api/router/duplicate_route_with_replace',
                              view_func=mock_view_function,
                              methods=HTTPMethodEnum.POST,
                              permissions=permissions,
                              login_required=True)

    router_services.add_route('/tests/api/router/duplicate_route_with_replace',
                              view_func=mock_view_function,
                              methods=(HTTPMethodEnum.GET, HTTPMethodEnum.PUT),
                              login_required=False,
                              max_content_length=123,
                              permissions=permissions,
                              replace=True)

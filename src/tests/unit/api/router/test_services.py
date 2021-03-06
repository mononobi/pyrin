# -*- coding: utf-8 -*-
"""
router test_services module.
"""

import pytest

import pyrin.api.router.services as router_services

from pyrin.api.router.exceptions import RouteAuthenticationMismatchError
from pyrin.api.router.handlers.protected import FreshProtectedRoute, ProtectedRoute
from pyrin.api.router.handlers.public import PublicRoute
from pyrin.api.schema.structs import ResultSchema
from pyrin.application.exceptions import DuplicateRouteURLError
from pyrin.core.enumerations import HTTPMethodEnum
from pyrin.core.globals import SECURE_FALSE, SECURE_TRUE
from pyrin.api.router.handlers.exceptions import MaxContentLengthLimitMismatchError, \
    InvalidViewFunctionTypeError, PermissionTypeError

from tests.unit.security.permission.base import PermissionMock
from tests.unit.common.mock_functions import mock_view_function


def test_create_route_fresh_protected():
    """
    creates the appropriate route based on the input parameters.
    it should create a fresh protected route.
    it should not have a result schema.
    """

    route = router_services.create_route('/api/router/fresh_protected',
                                         methods=HTTPMethodEnum.GET,
                                         view_function=mock_view_function,
                                         fresh_auth=True,
                                         max_content_length=15000,
                                         authenticated=True)

    assert isinstance(route, FreshProtectedRoute)
    assert route.result_schema is None


def test_create_route_public():
    """
    creates the appropriate route based on the input parameters.
    it should create a public route.
    """

    route = router_services.create_route('/api/router/public',
                                         methods=HTTPMethodEnum.POST,
                                         view_function=mock_view_function,
                                         authenticated=False,
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
                                         permissions=permissions,
                                         authenticated=True)

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
                                         fresh_auth=True,
                                         permissions=permission,
                                         authenticated=True)

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
                                             permissions=permissions,
                                             authenticated=True)


def test_create_route_with_mismatch_authentication():
    """
    creates the appropriate route based on the input parameters.
    it should raise an error due to mismatch in authentication options.
    """

    with pytest.raises(RouteAuthenticationMismatchError):
        route = router_services.create_route('/api/router/mismatch_protected',
                                             methods=HTTPMethodEnum.GET,
                                             view_function=mock_view_function,
                                             fresh_auth=True,
                                             authenticated=False,
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
                                             fresh_auth=True,
                                             authenticated=True,
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
                                             fresh_auth=False,
                                             authenticated=False)


def test_create_route_validate_max_content_length():
    """
    creates the appropriate route based on the input parameters.
    then validates the specified max content length.
    """

    route = router_services.create_route('/api/router/check_max_content',
                                         methods=HTTPMethodEnum.PUT,
                                         view_function=mock_view_function,
                                         fresh_auth=False,
                                         authenticated=False,
                                         max_content_length=12345)

    assert route.max_content_length == 12345


def test_create_route_with_schema_attributes():
    """
    creates the appropriate route with provided schema attributes.
    """

    route = router_services.create_route('/api/router/public_with_depth_and_readable',
                                         methods=HTTPMethodEnum.POST,
                                         view_function=mock_view_function,
                                         authenticated=False,
                                         depth=3,
                                         readable=SECURE_FALSE)

    assert route is not None
    assert route.result_schema is not None
    assert route.result_schema.depth == 3
    assert route.result_schema.readable is SECURE_FALSE


def test_create_route_with_schema():
    """
    creates the appropriate route with provided schema.
    """

    schema = ResultSchema(columns=['id', 'name', 'age'],
                          rename=dict(id='new_id', name='new_name'),
                          exclude=['extra'],
                          readable=SECURE_FALSE,
                          depth=5)

    route = router_services.create_route('/api/router/public_with_schema',
                                         methods=HTTPMethodEnum.POST,
                                         view_function=mock_view_function,
                                         authenticated=False,
                                         result_schema=schema)

    assert route is not None
    assert route.result_schema is not None
    assert route.result_schema is schema


def test_create_route_with_schema_with_overridden_attributes():
    """
    creates the appropriate route with provided schema and overridden attributes.
    """

    schema = ResultSchema(columns=['id', 'name', 'age'],
                          rename=dict(id='new_id', name='new_name'),
                          exclude=['extra'],
                          readable=SECURE_FALSE,
                          depth=0)

    route = router_services.create_route('/api/router/public_with_schema_overridden',
                                         methods=HTTPMethodEnum.POST,
                                         view_function=mock_view_function,
                                         authenticated=False,
                                         result_schema=schema,
                                         depth=4,
                                         readable=SECURE_TRUE)

    assert route is not None
    assert route.result_schema is not None
    assert route.result_schema is not schema
    assert route.result_schema.depth == 4
    assert route.result_schema.readable is SECURE_TRUE
    assert route.result_schema.columns == schema.columns
    assert route.result_schema.exclude == schema.exclude
    assert route.result_schema.rename == schema.rename

    assert schema.readable is SECURE_FALSE
    assert schema.depth == 0


def test_create_route_with_depth():
    """
    creates the appropriate route with provided depth.
    """

    route = router_services.create_route('/api/router/public_with_depth',
                                         methods=HTTPMethodEnum.POST,
                                         view_function=mock_view_function,
                                         authenticated=False,
                                         depth=8)

    assert route is not None
    assert route.result_schema is not None
    assert route.result_schema.depth == 8
    assert route.result_schema.readable is None


def test_create_route_with_readable():
    """
    creates the appropriate route with provided readable.
    """

    route = router_services.create_route('/api/router/public_with_readable',
                                         methods=HTTPMethodEnum.POST,
                                         view_function=mock_view_function,
                                         authenticated=False,
                                         readable=SECURE_FALSE)

    assert route is not None
    assert route.result_schema is not None
    assert route.result_schema.depth is None
    assert route.result_schema.readable is SECURE_FALSE


def test_add_route():
    """
    adds a new protected route in application routes.
    """

    permission = PermissionMock(104, 'permission_104')
    router_services.add_route('/tests/api/router/fake_route',
                              view_func=mock_view_function,
                              methods=HTTPMethodEnum.GET,
                              permissions=permission,
                              authenticated=True)


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
                                  authenticated=True)

        router_services.add_route('/tests/api/router/duplicate_route',
                                  view_func=mock_view_function,
                                  methods=HTTPMethodEnum.GET,
                                  authenticated=False,
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
                              authenticated=True)

    router_services.add_route('/tests/api/router/duplicate_route_with_replace',
                              view_func=mock_view_function,
                              methods=(HTTPMethodEnum.GET, HTTPMethodEnum.PUT),
                              authenticated=False,
                              max_content_length=123,
                              permissions=permissions,
                              replace=True)

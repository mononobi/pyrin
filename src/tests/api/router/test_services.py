# -*- coding: utf-8 -*-
"""
router test_services module.
"""

import pytest

import pyrin.api.router.services as router_services
import pyrin.utils.unique_id as id_utils

from pyrin.api.router.exceptions import RouteAuthenticationMismatchError
from pyrin.api.router.handlers.protected import FreshProtectedRoute, ProtectedRoute
from pyrin.api.router.handlers.public import PublicRoute
from pyrin.core.enumerations import HTTPMethodEnum
from pyrin.api.router.handlers.exceptions import MaxContentLengthLimitMismatchError, \
    InvalidViewFunctionTypeError, PermissionTypeError

from tests.common.mock_context import PermissionMock
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
    permissions.append(PermissionMock(id_utils.generate_uuid4()))
    permissions.append(PermissionMock(id_utils.generate_uuid4()))

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

    permission = PermissionMock(id_utils.generate_uuid4())
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
        permissions.append(PermissionMock(id_utils.generate_uuid4()))
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


def test_create_route_with_invalid_content_length():
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

    assert route.get_max_content_length() == 12345


def add_route(url, endpoint=None, view_func=None,
              provide_automatic_options=None, **options):
    """
    connects a url rule. if a view_func is provided it will be registered with the endpoint.
    if there is another rule with the same url and `replace=True` option is provided,
    it will be replaced, otherwise an error will be raised.

    :param str url: the url rule as string.

    :param str endpoint: the endpoint for the registered url rule.
                         pyrin itself assumes the url rule as endpoint.

    :param callable view_func: the function to call when serving a request to the
                               provided endpoint.

    :param bool provide_automatic_options: controls whether the `OPTIONS` method should be
                                           added automatically.
                                           this can also be controlled by setting the
                                           `view_func.provide_automatic_options = False`
                                           before adding the rule.

    :keyword tuple(str) methods: http methods that this rule should handle.
                                 if not provided, defaults to `GET`.

    :keyword tuple(PermissionBase) permissions: tuple of all required permissions
                                                to access this route's resource.

    :keyword bool login_required: specifies that this route could not be accessed
                                  if the requester has not a valid token.
                                  defaults to True if not provided.

    :keyword bool fresh_token: specifies that this route could not be accessed
                               if the requester has not a valid fresh token.
                               fresh token means a token that has been created by
                               providing user credentials to server.
                               defaults to False if not provided.

    :keyword bool replace: specifies that this route must replace
                           any existing route with the same url or raise
                           an error if not provided. defaults to False.

    :keyword int max_content_length: max content length that this route could handle,
                                     in bytes. if not provided, it will be set to
                                     `restricted_max_content_length` api config key.
                                     note that this value should be lesser than or equal
                                     to `max_content_length` api config key, otherwise
                                     it will cause an error.

    :raises DuplicateRouteURLError: duplicate route url error.
    """

    return get_component(RouterPackage.COMPONENT_NAME).add_route(url, endpoint, view_func,
                                                                 provide_automatic_options,
                                                                 **options)

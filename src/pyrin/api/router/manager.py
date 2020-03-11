# -*- coding: utf-8 -*-
"""
router manager module.
"""

import pyrin.application.services as application_services

from pyrin.api.router.exceptions import RouteAuthenticationMismatchError
from pyrin.api.router.handlers.protected import ProtectedRoute, FreshProtectedRoute
from pyrin.api.router.handlers.public import PublicRoute
from pyrin.core.context import Manager


class RouterManager(Manager):
    """
    router manager class.
    """

    def create_route(self, rule, **options):
        """
        creates the appropriate route based on the input parameters.

        :param str rule: unique url rule to register this route for.
                         routes with duplicated urls will be overwritten
                         if `replace=True` option is provided, otherwise an error
                         will be raised.

        :keyword tuple(str) methods: http methods that this route could handle.
                                     if not provided, defaults to `GET`, `HEAD`
                                     and `OPTIONS`.

        :keyword callable view_function: a function to be called on accessing this route.

        :keyword str endpoint: the endpoint for the registered url rule. pyrin
                               itself assumes the url rule as endpoint if not provided.

        :keyword bool login_required: specifies that this route could not be accessed
                                      if the requester has not a valid token.
                                      defaults to True if not provided.

        :keyword bool fresh_token: specifies that this route could not be accessed
                                   if the requester has not a valid fresh token.
                                   fresh token means a token that has been created by
                                   providing user credentials to server.
                                   defaults to False if not provided.

        :keyword tuple(PermissionBase) permissions: tuple of all required permissions
                                                    to access this route's resource.

        :keyword int max_content_length: max content length that this route could handle,
                                         in bytes. if not provided, it will be set to
                                         `restricted_max_content_length` api config key.
                                         note that this value should be lesser than or equal
                                         to `max_content_length` api config key, otherwise
                                         it will cause an error.

        :raises RouteAuthenticationMismatchError: route authentication mismatch error.

        :rtype: RouteBase
        """

        route = self._create_route(rule, **options)
        if route is not None:
            return route

        login_required = options.get('login_required', True)
        fresh_token = options.get('fresh_token', False)

        if login_required is False and fresh_token is False:
            return PublicRoute(rule, **options)
        elif login_required is True and fresh_token is False:
            return ProtectedRoute(rule, **options)
        elif login_required is True and fresh_token is True:
            return FreshProtectedRoute(rule, **options)
        else:
            raise RouteAuthenticationMismatchError('"login_required={login}" and '
                                                   '"fresh_token={fresh}" in route '
                                                   '[{route}] are incompatible.'
                                                   .format(login=login_required,
                                                           fresh=fresh_token,
                                                           route=rule))

    def _create_route(self, rule, **options):
        """
        creates the appropriate route based on the input parameters.
        this method is intended to be overridden by subclasses to provided
        custom `RouteBase` types, it should always return a `RouteBase`
        object or `None`.

        :param str rule: unique url rule to register this route for.
                         routes with duplicated urls will be overwritten
                         if `replace=True` option is provided, otherwise an error
                         will be raised.

        :keyword tuple(str) methods: http methods that this route could handle.
                                     if not provided, defaults to `GET`, `HEAD`
                                     and `OPTIONS`.

        :keyword callable view_function: a function to be called on accessing this route.

        :keyword str endpoint: the endpoint for the registered url rule. pyrin
                               itself assumes the url rule as endpoint if not provided.

        :keyword bool login_required: specifies that this route could not be accessed
                                      if the requester has not a valid token.
                                      defaults to True if not provided.

        :keyword bool fresh_token: specifies that this route could not be accessed
                                   if the requester has not a valid fresh token.
                                   fresh token means a token that has been created by
                                   providing user credentials to server.
                                   defaults to False if not provided.

        :keyword tuple(PermissionBase) permissions: tuple of all required permissions
                                                    to access this route's resource.

        :keyword int max_content_length: max content length that this route could handle,
                                         in bytes. if not provided, it will be set to
                                         `restricted_max_content_length` api config key.
                                         note that this value should be lesser than or equal
                                         to `max_content_length` api config key, otherwise
                                         it will cause an error.

        :rtype: RouteBase
        """

        return None

    def add_route(self, url, endpoint=None, view_func=None,
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

        application_services.add_url_rule(url, endpoint=endpoint, view_func=view_func,
                                          provide_automatic_options=provide_automatic_options,
                                          **options)

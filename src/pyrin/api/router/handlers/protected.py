# -*- coding: utf-8 -*-
"""
protected route handler module.
"""

import pyrin.security.authorization.services as authorization_services
import pyrin.security.session.services as session_services

from pyrin.api.router.handlers.base import RouteBase
from pyrin.api.router.handlers.exceptions import FreshTokenRequiredError, PermissionTypeError
from pyrin.core.globals import _, LIST_TYPES
from pyrin.security.permission.base import PermissionBase


class ProtectedRoute(RouteBase):
    """
    protected route class.
    this class should be used to manage application protected api routes that need valid token.
    """

    def __init__(self, rule, **options):
        """
        initializes a new instance of ProtectedRoute.

        :param str rule: unique url rule to register this route for.
                         routes with duplicated urls will be overwritten
                         if `replace=True` option is provided, otherwise an error
                         will be raised.

        :keyword tuple(str) methods: http methods that this route could handle.
                                     if not provided, defaults to `GET`, `HEAD`
                                     and `OPTIONS`.

        :keyword callable view_function: a function to be called on accessing this route.

        :keyword str endpoint: the endpoint for the registered url rule. pyrin
                               itself assumes the rule as endpoint if not provided.

        :keyword dict defaults: an optional dict with defaults for other rules with the same
                                endpoint. this is a bit tricky but useful if you want
                                to have unique urls.

        :keyword str subdomain: the subdomain rule string for this rule. If not specified the rule
                                only matches for the `default_subdomain` of the map. if the map is
                                not bound to a subdomain this feature is disabled.

        :keyword bool strict_slashes: override the `Map` setting for `strict_slashes` only
                                      for this rule. if not specified the `Map` setting is used.

        :keyword bool build_only: set this to True and the rule will never match but will
                                  create a url that can be build. this is useful if you
                                  have resources on a subdomain or folder that are not
                                  handled by the WSGI application (like static data)

        :keyword Union[string, Callable] redirect_to: if given this must be either a string or
                                                      callable. in case of a callable it's
                                                      called with the url adapter that triggered
                                                      the match and the values of the url as
                                                      keyword arguments and has to return the
                                                      target for the redirect, otherwise it
                                                      has to be a string with placeholders
                                                      in rule syntax.

        :keyword bool alias: if enabled this rule serves as an alias for another rule with
                             the same endpoint and arguments.

        :keyword str host: if provided and the url map has host matching enabled this can be
                           used to provide a match rule for the whole host. this also means
                           that the subdomain feature is disabled.
                               
        :keyword tuple(PermissionBase) permissions: tuple of all required permissions
                                                    to access this route's resource.

        :keyword int max_content_length: max content length that this route could handle,
                                         in bytes. if not provided, it will be set to
                                         `restricted_max_content_length` api config key.
                                         note that this value should be lesser than or equal
                                         to `max_content_length` api config key, otherwise
                                         it will cause an error.

        :raises MaxContentLengthLimitMismatchError: max content length limit mismatch error.
        :raises InvalidViewFunctionTypeError: invalid view function type error.
        :raises PermissionTypeError: permission type error.
        """

        super().__init__(rule, **options)

        self._permissions = options.get('permissions', ())
        if not isinstance(self._permissions, LIST_TYPES):
            self._permissions = (self._permissions,)

        if not all(isinstance(item, PermissionBase) for item in self._permissions):
            raise PermissionTypeError('All route permissions must be an '
                                      'instance of PermissionBase.')

    def _handle(self, inputs, **options):
        """
        handles the current route.
        routes which need to perform extra operations before
        view function execution, must override this method.

        :param dict inputs: view function inputs.

        :raises UserNotAuthenticatedError: user not authenticated error.
        :raises UserIsNotActiveError: user is not active error.
        :raises AuthorizationFailedError: authorization failed error.
        """

        self._authorize()

    def _authorize(self):
        """
        authorizes the route permissions for current user.

        :raises UserNotAuthenticatedError: user not authenticated error.
        :raises UserIsNotActiveError: user is not active error.
        :raises AuthorizationFailedError: authorization failed error.
        """

        user = session_services.get_current_user()
        authorization_services.authorize(user, self.get_permissions())

    def get_permissions(self):
        """
        gets all required permissions to access this route.

        :returns: tuple(PermissionBase)

        :rtype: tuple
        """

        return self._permissions


class FreshProtectedRoute(ProtectedRoute):
    """
    fresh protected route class.
    this class should be used to manage application protected api routes that
    need valid fresh token. fresh token means a token that has been created
    by providing user credentials to server.
    """

    def __init__(self, rule, **options):
        """
        initializes a new instance of FreshProtectedRoute.

        :param str rule: unique url rule to register this route for.
                         routes with duplicated urls will be overwritten
                         if `replace=True` option is provided, otherwise an error
                         will be raised.

        :keyword tuple(str) methods: http methods that this route could handle.
                                     if not provided, defaults to `GET`, `HEAD`
                                     and `OPTIONS`.

        :keyword callable view_function: a function to be called on accessing this route.

        :keyword str endpoint: the endpoint for the registered url rule. pyrin
                               itself assumes the rule as endpoint if not provided.

        :keyword dict defaults: an optional dict with defaults for other rules with the same
                                endpoint. this is a bit tricky but useful if you want
                                to have unique urls.

        :keyword str subdomain: the subdomain rule string for this rule. If not specified the rule
                                only matches for the `default_subdomain` of the map. if the map is
                                not bound to a subdomain this feature is disabled.

        :keyword bool strict_slashes: override the `Map` setting for `strict_slashes` only
                                      for this rule. if not specified the `Map` setting is used.

        :keyword bool build_only: set this to True and the rule will never match but will
                                  create a url that can be build. this is useful if you
                                  have resources on a subdomain or folder that are not
                                  handled by the WSGI application (like static data)

        :keyword Union[string, Callable] redirect_to: if given this must be either a string or
                                                      callable. in case of a callable it's
                                                      called with the url adapter that triggered
                                                      the match and the values of the url as
                                                      keyword arguments and has to return the
                                                      target for the redirect, otherwise it
                                                      has to be a string with placeholders
                                                      in rule syntax.

        :keyword bool alias: if enabled this rule serves as an alias for another rule with
                             the same endpoint and arguments.

        :keyword str host: if provided and the url map has host matching enabled this can be
                           used to provide a match rule for the whole host. this also means
                           that the subdomain feature is disabled.

        :keyword tuple(PermissionBase) permissions: tuple of all required permissions
                                                    to access this route's resource.

        :keyword int max_content_length: max content length that this route could handle,
                                         in bytes. if not provided, it will be set to
                                         `restricted_max_content_length` api config key.
                                         note that this value should be lesser than or equal
                                         to `max_content_length` api config key, otherwise
                                         it will cause an error.

        :raises MaxContentLengthLimitMismatchError: max content length limit mismatch error.
        :raises InvalidViewFunctionTypeError: invalid view function type error.
        :raises PermissionTypeError: permission type error.
        """

        super().__init__(rule, **options)

    def _authorize(self):
        """
        authorizes the route permissions for current user.
        also checks that the user has a fresh token.

        :raises FreshTokenRequiredError: fresh token required error.
        :raises UserNotAuthenticatedError: user not authenticated error.
        :raises UserIsNotActiveError: user is not active error.
        :raises AuthorizationFailedError: authorization failed error.
        """

        if not session_services.is_fresh():
            raise FreshTokenRequiredError(_('Fresh token is required to '
                                            'access the requested resource.'))

        super()._authorize()

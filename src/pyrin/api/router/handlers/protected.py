# -*- coding: utf-8 -*-
"""
protected route handler module.
"""

from pyrin.api.router.handlers.base import RouteBase


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
        """

        super(ProtectedRoute, self).__init__(rule, **options)

        self._permissions = options.get('permissions', ())
        if not isinstance(self._permissions, (tuple, list, set)):
            self._permissions = (self._permissions,)

    def is_login_required(self):
        """
        gets a value indicating that accessing this route needs a valid token.

        :rtype: bool
        """

        return True

    def dispatch(self, request, **options):
        """
        dispatch the current route.

        :param CoreRequest request: current request object.

        :returns: view function's result.

        :rtype: object
        """

        return super(ProtectedRoute, self).dispatch(request, **options)


class SimpleProtectedRoute(ProtectedRoute):
    """
    simple protected route class.
    this class just passes the `request.view_args` to the view function as input params.
    """

    def __init__(self, rule, **options):
        """
        initializes a new instance of SimpleProtectedRoute.

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

        :keyword dict defaults: an optional dict with defaults for other rules with the
                                same endpoint. this is a bit tricky but useful if you
                                want to have unique urls.

        :keyword str subdomain: the subdomain rule string for this rule. If not specified the rule
                                only matches for the `default_subdomain` of the map. if the map is
                                not bound to a subdomain this feature is disabled.

        :keyword bool strict_slashes: override the `Map` setting for `strict_slashes` only
                                      for this rule. if not specified the `Map` setting is used.

        :keyword bool build_only: set this to True and the rule will never match but will
                                  create a url that can be build. this is useful if you have
                                  resources on a subdomain or folder that are not handled by
                                  the WSGI application (like static data)

        :keyword Union[string, Callable] redirect_to: if given this must be either a string
                                                      or callable. in case of a callable it's
                                                      called with the url adapter that triggered
                                                      the match and the values of the url as
                                                      keyword arguments and has to return the
                                                      target for the redirect, otherwise it has
                                                      to be a string with placeholders
                                                      in rule syntax.

        :keyword bool alias: if enabled this rule serves as an alias for another rule with
                             the same endpoint and arguments.

        :keyword str host: if provided and the url map has host matching enabled this can be
                           used to provide a match rule for the whole host. this also means
                           that the subdomain feature is disabled.

        :keyword tuple(PermissionBase) permissions: tuple of all required permissions
                                                    to access this route's resource.
        """

        super(SimpleProtectedRoute, self).__init__(rule, **options)

    def _call_view_function(self, request, **options):
        """
        calls the route's view function.

        :param CoreRequest request: current request object.

        :returns: view function's result.

        :rtype: object
        """

        return self._view_function(**(request.view_args or {}))

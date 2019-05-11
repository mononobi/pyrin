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

        :keyword list[str] methods: http methods that this route could handle.
                                    if not provided, defaults to `GET`, `HEAD`
                                    and `OPTIONS`.
                        
        :keyword callable view_func: a function to be called on accessing this route.

        :keyword str endpoint: the endpoint for the registered url rule. flask
                               itself assumes the name of the view function as
                               endpoint if not provided.
                               
        :keyword tuple(PermissionBase) permissions: tuple of all required permissions
                                                    to access this route's resource.

        """

        super(ProtectedRoute, self).__init__(rule, **options)

        self._permissions = options.get('permissions', ())
        if not isinstance(self._permissions, (tuple, list, set)):
            self._permissions = (self._permissions,)

    def get_permissions(self, **options):
        """
        gets this route's required permissions.

        :rtype: tuple(PermissionBase)
        """

        return self._permissions

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
        """

        pass

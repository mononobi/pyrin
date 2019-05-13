# -*- coding: utf-8 -*-
"""
router manager module.
"""

from pyrin.api.router.handlers.protected import ProtectedRoute
from pyrin.api.router.handlers.public import PublicRoute
from pyrin.context import CoreObject


class RouterManager(CoreObject):
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

        :keyword list[str] methods: http methods that this route could handle.
                                    if not provided, defaults to `GET`, `HEAD`
                                    and `OPTIONS`.

        :keyword callable view_function: a function to be called on accessing this route.

        :keyword str endpoint: the endpoint for the registered url rule. pyrin
                               itself assumes the url rule as endpoint if not provided.

        :keyword bool login_required: specifies that this route could not be accessed
                                      if the requester has not a valid token.
                                      defaults to True if not provided.

        :keyword tuple(PermissionBase) permissions: tuple of all required permissions
                                                    to access this route's resource.

        :rtype: RouteBase
        """

        login_required = options.get('login_required', True)

        if login_required is False:
            return PublicRoute(rule, **options)
        else:
            return ProtectedRoute(rule, **options)

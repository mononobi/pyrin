# -*- coding: utf-8 -*-
"""
router decorators module.
"""

import pyrin.application.services as application_services


def api(url, **options):
    """
    decorator to register an api handler for application.

    :param str url: url rule for this api.

    :keyword tuple(str) methods: http methods that this rule should handle.
                                 if not provided, defaults to `GET`.

    :keyword tuple(PermissionBase) permissions: tuple of all required permissions
                                                to access this route's resource.

    :keyword bool login_required: specifies that this route could not be accessed
                                  if the requester has not a valid token.
                                  defaults to True if not provided.

    :keyword bool replace: specifies that this route must replace
                           any existing route with the same url or raise
                           an error if not provided. defaults to False.

    :rtype: callable
    """

    def decorator(func):
        """
        decorates the given function and registers it as an api handler.

        :param callable func: function to register it as an api handler.

        :rtype: callable
        """

        application_services.add_url_rule(url, view_func=func, **options)

        return func

    return decorator

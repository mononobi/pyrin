# -*- coding: utf-8 -*-
"""
router decorators module.
"""

import pyrin.api.router.services as router_services


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

    :rtype: callable
    """

    def decorator(func):
        """
        decorates the given function and registers it as an api handler.

        :param callable func: function to register it as an api handler.

        :rtype: callable
        """

        router_services.add_route(url, view_func=func, **options)

        return func

    return decorator

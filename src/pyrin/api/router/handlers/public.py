# -*- coding: utf-8 -*-
"""
public route handler module.
"""

from pyrin.api.router.handlers.base import RouteBase


class PublicRoute(RouteBase):
    """
    public route class.
    this class should be used to manage application public api routes that does not need valid token.
    """

    def __init__(self, rule, **options):
        """
        initializes a new instance of PublicRoute.

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
        """

        super(PublicRoute, self).__init__(rule, **options)

    def is_login_required(self):
        """
        gets a value indicating that accessing this route needs a valid token.

        :rtype: bool
        """

        return False

    def dispatch(self, request, **options):
        """
        dispatch the current route.

        :param CoreRequest request: current request object.
        """

        pass

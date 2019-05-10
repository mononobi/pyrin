# -*- coding: utf-8 -*-
"""
route module.
"""

from pyrin.api.router.base import RouteBase


class Route(RouteBase):
    """
    route class.
    this class should be used to manage application api routes.
    """

    def __init__(self, rule, **options):
        """
        initializes a new instance of Route.

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
                                                    
        :keyword bool login_required: specifies that this route could not be accessed
                                      if the requester has not a valid token.
                                      defaults to True if not provided.
         
        :keyword bool replace: specifies that this route must replace
                               any existing route with the same url or raise
                               an error if not provided. defaults to False.
        """

        super(Route, self).__init__(rule, **options)

    def dispatch(self, request, **options):
        """
        dispatch the current route.

        :param CoreRequest request: current request object.
        """

        pass

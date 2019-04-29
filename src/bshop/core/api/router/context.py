# -*- coding: utf-8 -*-
"""
router context module.
"""

from bshop.core.context import CoreObject


class Route(CoreObject):
    """
    route class.
    this class should be used to manage application api routes.
    """

    def __init__(self, url, view_function, http_methods, **option):
        """
        initializes a new instance of Route.

        :param str url: unique url to register this route for.
                        routes with duplicated urls will be overridden
                        if `replace=True` option is provided. defaults to False.
                        
        :param callable view_function: a function to be called on accessing this route.

        :param tuple(str) http_methods: http methods that this route could handle.
                                        if not provided, defaults to `GET`, `HEAD`
                                        and `OPTIONS`.

        :keyword str endpoint: the endpoint for the registered url rule. flask
                               itself assumes the name of the view function as
                               endpoint if not provided.
                               
        :keyword tuple(PermissionBase) permissions: list of all required permissions
                                                    to access this route's resource.
                                                    
        :keyword bool login_required: specifies that this route could not be accessed
                                      if the requester has not a valid token.
                                      defaults to True if not provided.
         
        :keyword bool replace: specifies that this route must replace
                               any existing route with the same url parameter or
                               raise an error if not provided. defaults to False.
        """

        CoreObject.__init__(self)

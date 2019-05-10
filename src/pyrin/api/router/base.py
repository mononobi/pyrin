# -*- coding: utf-8 -*-
"""
router base module.
"""

from werkzeug.routing import Rule

from pyrin.exceptions import CoreNotImplementedError


class RouteBase(Rule):
    """
    route base class.
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

        # we should call super method with exact param names because it
        # does not have `**options` in it's signature and raises an error
        # if extra keywords passed to it. maybe flask fixes it in the future.
        super(RouteBase, self).__init__(rule,
                                        defaults=options.get('defaults', None),
                                        subdomain=options.get('subdomain', None),
                                        methods=options.get('methods', None),
                                        build_only=options.get('build_only', False),
                                        endpoint=options.get('endpoint', None),
                                        strict_slashes=options.get('strict_slashes', None),
                                        redirect_to=options.get('redirect_to', None),
                                        alias=options.get('alias', False),
                                        host=options.get('host', None))

        self._permissions = options.get('permissions', ())
        if not isinstance(self._permissions, (tuple, list, set)):
            self._permissions = (self._permissions,)

        self._login_required = options.get('login_required', True)
        self._replace = options.get('replace', False)

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

        return self._login_required

    def allow_replace(self):
        """
        gets a value indicating that if there is an already available route with the same url,
        it should be replaced by the new one, otherwise raises an error.

        :rtype: bool
        """

        return self._replace

    def dispatch(self, request, **options):
        """
        dispatch the current route.

        :param CoreRequest request: current request object.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

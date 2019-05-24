# -*- coding: utf-8 -*-
"""
route base handler module.
"""

from werkzeug.routing import Rule

from pyrin.api.router.handlers.exceptions import InvalidViewFunctionTypeError
from pyrin.context import DTO
from pyrin.exceptions import CoreNotImplementedError


class RouteBase(Rule):
    """
    route base class.
    """

    def __init__(self, rule, **options):
        """
        initializes a new instance of RouteBase.

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
                                same endpoint.
                                this is a bit tricky but useful if you want to have unique urls.

        :keyword str subdomain: the subdomain rule string for this rule. If not specified the rule
                                only matches for the `default_subdomain` of the map. if the map is
                                not bound to a subdomain this feature is disabled.

        :keyword bool strict_slashes: override the `Map` setting for `strict_slashes` only for
                                      this rule. if not specified the `Map` setting is used.

        :keyword bool build_only: set this to True and the rule will never match but will
                                  create a url that can be build. this is useful if you have
                                  resources on a subdomain or folder that are not handled by
                                  the WSGI application (like static data)

        :keyword Union[string, Callable] redirect_to: if given this must be either a string
                                                      or callable. in case of a callable it's
                                                      called with the url adapter that
                                                      triggered the match and the values
                                                      of the url as keyword arguments and has
                                                      to return the target for the redirect,
                                                      otherwise it has to be a string with
                                                      placeholders in rule syntax.

        :keyword bool alias: if enabled this rule serves as an alias for another rule with
                             the same endpoint and arguments.

        :keyword str host: if provided and the url map has host matching enabled this can be
                           used to provide a match rule for the whole host. this also means
                           that the subdomain feature is disabled.

        :raises InvalidViewFunctionTypeError: invalid view function type error.
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

        self._view_function = options.get('view_function')

        if not callable(self._view_function):
            raise InvalidViewFunctionTypeError('The provided view function [{function}] '
                                               'for route [{route}] is not callable.'
                                               .format(function=str(self._view_function),
                                                       route=str(self)))

    def is_login_required(self):
        """
        gets a value indicating that accessing this route needs a valid token.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    def dispatch(self, request, **options):
        """
        dispatch the current route.

        :param CoreRequest request: current request object.
        """

        return self._call_view_function(request, **options)

    def _call_view_function(self, request, **options):
        """
        calls the route's view function.

        :param CoreRequest request: current request object.

        :returns: view function's result.

        :rtype: object
        """

        method_inputs = DTO(**(request.view_args or {}),
                            **(request.get_json(force=True, silent=True) or {}),
                            query_params=request.args,
                            files=request.files)

        return self._view_function(**method_inputs)

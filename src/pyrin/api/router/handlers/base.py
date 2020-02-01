# -*- coding: utf-8 -*-
"""
route base handler module.
"""

from werkzeug.routing import Rule

import pyrin.configuration.services as config_services
import pyrin.security.session.services as session_services

from pyrin.core.globals import _, LIST_TYPES
from pyrin.api.router.handlers.exceptions import InvalidViewFunctionTypeError, \
    MaxContentLengthLimitMismatchError, LargeContentError


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

        :keyword int max_content_length: max content length that this route could handle,
                                         in bytes. if not provided, it will be set to
                                         `restricted_max_content_length` api config key.
                                         note that this value should be lesser than or equal
                                         to `max_content_length` api config key, otherwise
                                         it will cause an error.

        :raises MaxContentLengthLimitMismatchError: max content length limit mismatch error.
        :raises InvalidViewFunctionTypeError: invalid view function type error.
        """

        methods = options.get('methods', ())
        if not isinstance(methods, LIST_TYPES):
            methods = (methods,)
            options.update(methods=methods)

        # we should call super method with exact param names because it
        # does not have `**options` in it's signature and raises an error
        # if extra keywords passed to it. maybe flask fixes it in the future.
        super().__init__(rule,
                         defaults=options.get('defaults', None),
                         subdomain=options.get('subdomain', None),
                         methods=methods,
                         build_only=options.get('build_only', False),
                         endpoint=options.get('endpoint', None),
                         strict_slashes=options.get('strict_slashes', None),
                         redirect_to=options.get('redirect_to', None),
                         alias=options.get('alias', False),
                         host=options.get('host', None))

        self._view_function = options.get('view_function')

        global_limit = config_services.get('api', 'general', 'max_content_length')

        restricted_length = options.get('max_content_length',
                                        config_services.get('api',
                                                            'general',
                                                            'restricted_max_content_length'))

        if restricted_length > global_limit:
            raise MaxContentLengthLimitMismatchError('Specified max content length '
                                                     '[{restricted}] for route [{route}] is '
                                                     'greater than global limit which is '
                                                     '[{global_limit}].'
                                                     .format(restricted=restricted_length,
                                                             route=rule,
                                                             global_limit=global_limit))

        self._max_content_length = restricted_length

        if not callable(self._view_function):
            raise InvalidViewFunctionTypeError('The provided view function [{function}] '
                                               'for route [{route}] is not callable.'
                                               .format(function=str(self._view_function),
                                                       route=str(self)))

    def handle(self, inputs, **options):
        """
        handles the current route.

        :param dict inputs: view function inputs.

        :raises LargeContentError: large content error.

        :returns: view function's result.

        :rtype: object
        """

        self._validate_content_length()
        self._handle(inputs, **options)

        return self._call_view_function(inputs, **options)

    def _handle(self, inputs, **options):
        """
        handles the current route.
        routes which need to perform extra operations before
        view function execution, must override this method.

        :param dict inputs: view function inputs.
        """
        pass

    def _validate_content_length(self):
        """
        validates content length for this route.

        :raises LargeContentError: large content error.
        """

        client_request = session_services.get_current_request()
        if client_request.safe_content_length > self.get_max_content_length():
            raise LargeContentError(_('Request content is too large.'))

    def _call_view_function(self, inputs, **options):
        """
        calls the route's view function.

        :param dict inputs: view function inputs.

        :returns: view function's result.

        :rtype: object
        """

        return self._view_function(**inputs)

    def get_view_function(self):
        """
        gets this route's view function.

        :rtype: callable
        """

        return self._view_function

    def get_max_content_length(self):
        """
        gets this route's max content bytes length.

        :rtype: int
        """

        return self._max_content_length

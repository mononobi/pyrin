# -*- coding: utf-8 -*-
"""
public route handler module.
"""

from pyrin.api.router.handlers.base import RouteBase


class PublicRoute(RouteBase):
    """
    public route class.
    this class should be used to manage application public api
    routes that does not need valid token.
    """

    def __init__(self, rule, **options):
        """
        initializes a new instance of PublicRoute.

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

        :keyword bool strict_slashes: override the `Map` setting for `strict_slashes` only
                                      for this rule. if not specified the `Map` setting is used.

        :keyword bool build_only: set this to True and the rule will never match but will
                                  create a url that can be build. this is useful if you have
                                  resources on a subdomain or folder that are not handled by
                                  the WSGI application (like static data)

        :keyword Union[string, Callable] redirect_to: if given this must be either a string
                                                      or callable. in case of a callable it's
                                                      called with the url adapter that triggered
                                                      the match and the values of the url as
                                                      keyword arguments and has to return the
                                                      target for the redirect, otherwise it
                                                      has to be a string with placeholders
                                                      in rule syntax.

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

        super().__init__(rule, **options)

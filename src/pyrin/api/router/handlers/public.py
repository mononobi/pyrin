# -*- coding: utf-8 -*-
"""
router handlers public module.
"""

import time

from pyrin.core.globals import _
from pyrin.api.router.handlers.base import RouteBase
from pyrin.api.router.handlers.exceptions import InvalidRequestLimitError, \
    InvalidLifetimeError, URLNotFoundError, RequestLimitOrLifetimeRequiredError


class PublicRoute(RouteBase):
    """
    public route class.

    this class should be used to manage application public api
    routes that do not require authentication.
    """
    pass


class PublicTemporaryRoute(PublicRoute):
    """
    public temporary route class.

    this class should be used to manage application public api
    routes that do not require authentication and must be unregistered
    after a specified number of requests or a duration of time.
    this is useful for a couple of different things but mostly for system
    health checking after each new deployment on production.
    """

    def __init__(self, rule, **options):
        """
        initializes an instance of PublicTemporaryRoute.

        :param str rule: unique url rule to register this route for.
                         routes with duplicated urls and http methods will be
                         overwritten if `replace=True` option is provided.
                         otherwise an error will be raised.

        :keyword int request_limit: number of allowed requests to this
                                    route before it unregisters itself.
                                    defaults to None if not Provided.

        :keyword int lifetime: number of seconds in which this route must remain
                               responsive after initial registration. after this
                               period, the route will unregister itself.
                               defaults to None if not provided.

        :note request_limit, lifetime: if both of these values are provided, this
                                       route will unregister itself if any of
                                       these two conditions are met.

        :keyword str | tuple[str] methods: http methods that this route could handle.
                                           if not provided, defaults to `GET`, `HEAD`
                                           and `OPTIONS`.

        :keyword function view_function: a function to be called on accessing this route.

        :keyword str endpoint: the endpoint for the registered url rule.

        :keyword dict defaults: an optional dict with defaults for other rules with the
                                same endpoint. this is a bit tricky but useful if you
                                want to have unique urls.

        :keyword str subdomain: the subdomain rule string for this rule. If not specified the
                                rule only matches for the `default_subdomain` of the map. if
                                the map is not bound to a subdomain this feature is disabled.

        :keyword bool strict_slashes: override the `Map` setting for `strict_slashes` only for
                                      this rule. if not specified the `Map` setting is used.

        :keyword bool merge_slashes: override `Map.merge_slashes` for this rule.

        :keyword bool build_only: set this to True and the rule will never match but will
                                  create a url that can be build. this is useful if you have
                                  resources on a subdomain or folder that are not handled by
                                  the WSGI application (like static data)

        :keyword str | callable redirect_to: if given this must be either a string
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

        :keyword bool websocket: if set to True, this rule is only matches for
                                 websocket (`ws://`, `wss://`) requests. by default,
                                 rules will only match for http requests.
                                 defaults to False if not provided.

        :keyword int max_content_length: max content length that this route could handle,
                                         in bytes. if not provided, it will be set to
                                         `restricted_max_content_length` api config key.
                                         note that this value should be lesser than or equal
                                         to `max_content_length` api config key, otherwise
                                         it will cause an error.

        :keyword int status_code: status code to be returned on successful responses.
                                  defaults to corresponding status code of request's
                                  http method if not provided.

        :note status_code: it could be a value from `InformationResponseCodeEnum`
                           or `SuccessfulResponseCodeEnum` or `RedirectionResponseCodeEnum`.

        :keyword bool strict_status: specifies that it should only consider
                                     the status code as processed if it is from
                                     `InformationResponseCodeEnum` or
                                     `SuccessfulResponseCodeEnum` or
                                     `RedirectionResponseCodeEnum` values. otherwise
                                     all codes from `INFORMATION_CODE_MIN`
                                     to `INFORMATION_CODE_MAX` or from
                                     `SUCCESS_CODE_MIN` to `SUCCESS_CODE_MAX`
                                     or from `REDIRECTION_CODE_MIN` to
                                     `REDIRECTION_CODE_MAX` will be considered
                                     as processed. defaults to True if not provided.

        :keyword ResultSchema result_schema: result schema to be used to filter results.

        :keyword SECURE_TRUE | SECURE_FALSE exposed_only: specifies that any column or attribute
                                                          which has `exposed=False` or its name
                                                          starts with underscore `_`, should not
                                                          be included in result dict. defaults
                                                          to `SECURE_TRUE` if not provided. it
                                                          will be used only for entity conversion.
                                                          this value will override the
                                                          corresponding value of `result_schema`
                                                          if provided.

        :keyword int depth: a value indicating the depth for conversion.
                            for example if entity A has a relationship with
                            entity B and there is a list of B in A, if `depth=0`
                            is provided, then just columns of A will be available
                            in result dict, but if `depth=1` is provided, then all
                            B entities in A will also be included in the result dict.
                            actually, `depth` specifies that relationships in an
                            entity should be followed by how much depth.
                            note that, if `columns` is also provided, it is required to
                            specify relationship property names in provided columns.
                            otherwise they won't be included even if `depth` is provided.
                            defaults to `default_depth` value of database config store.
                            please be careful on increasing `depth`, it could fail
                            application if set to higher values. choose it wisely.
                            normally the maximum acceptable `depth` would be 2 or 3.
                            there is a hard limit for max valid `depth` which is set
                            in `ConverterMixin.MAX_DEPTH` class variable. providing higher
                            `depth` value than this limit, will cause an error.
                            it will be used only for entity conversion.
                            this value will override the corresponding value of
                            `result_schema` if provided.

        :keyword bool no_cache: a value indicating that the response returning from this route
                                must have a `Cache-Control: no-cache` header. this header will
                                be automatically added. defaults to False if not provided.

        :raises MaxContentLengthLimitMismatchError: max content length limit mismatch error.
        :raises InvalidViewFunctionTypeError: invalid view function type error.
        :raises InvalidResultSchemaTypeError: invalid result schema type error.
        :raises InvalidResponseStatusCodeError: invalid response status code error.
        :raises InvalidRequestLimitError: invalid request limit error.
        :raises InvalidLifetimeError: invalid lifetime error.
        :raises RequestLimitOrLifetimeRequiredError: request limit or lifetime required error.
        """

        super().__init__(rule, **options)

        request_limit = options.get('request_limit')
        lifetime = options.get('lifetime')

        if request_limit is None and lifetime is None:
            raise RequestLimitOrLifetimeRequiredError('Request limit or lifetime must be '
                                                      'provided to define a temporary route.')

        if request_limit is not None and request_limit <= 0:
            raise InvalidRequestLimitError('Request limit for temporary routes '
                                           'must be a positive number.')

        if lifetime is not None and lifetime <= 0:
            raise InvalidLifetimeError('Lifetime for temporary routes must '
                                       'be a positive number of seconds.')

        self._lifetime = lifetime
        self._request_limit = request_limit
        self._registered_time = time.time()
        self._total_requests = 0

    def _is_request_limit_reached(self):
        """
        gets a value indicating that request count limit has been reached.

        :rtype: bool
        """

        if self._request_limit is not None:
            return self._total_requests >= self._request_limit

        return False

    def _is_lifetime_ended(self):
        """
        gets a value indicating that lifetime of this route has been ended.

        :rtype: bool
        """

        if self._lifetime is not None:
            return time.time() - self._registered_time >= self._lifetime

        return False

    def _should_unregister(self):
        """
        gets a value indicating that this route must be unregistered.

        :rtype: bool
        """

        return self._is_request_limit_reached() or self._is_lifetime_ended()

    def _increase_performed_requests(self):
        """
        increases performed request count of this route by one.
        """

        self._total_requests = self._total_requests + 1

    def _handle(self, inputs, **options):
        """
        handles the current route.

        :param dict inputs: view function inputs.

        :raises URLNotFoundError: url not found error.
        """

        if self._should_unregister() is True:
            self._unregister()
            raise URLNotFoundError(_('The requested URL was not found on the server. if you '
                                     'entered the URL manually please check your spelling and '
                                     'try again.'))

        self._increase_performed_requests()

    def _finished(self, result, **options):
        """
        does the extra required works after the view function has been executed.

        this method will unregister the route if the limit or lifetime has been reached.

        :param object result: view function execution result.
        """

        if self._should_unregister() is True:
            self._unregister()

    def _unregister(self):
        """
        unregisters current route from application.
        """
        pass

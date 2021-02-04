# -*- coding: utf-8 -*-
"""
router manager module.
"""

import pyrin.application.services as application_services
import pyrin.utils.misc as misc_utils

from pyrin.core.structs import Manager
from pyrin.api.router import RouterPackage
from pyrin.api.router.handlers.base import RouteBase
from pyrin.api.router.handlers.public import PublicRoute, PublicTemporaryRoute
from pyrin.api.router.handlers.protected import ProtectedRoute, FreshProtectedRoute, \
    ProtectedTemporaryRoute, FreshProtectedTemporaryRoute
from pyrin.api.router.exceptions import RouteAuthenticationMismatchError, \
    InvalidCustomRouteTypeError


class RouterManager(Manager):
    """
    router manager class.
    """

    package_class = RouterPackage

    def create_route(self, rule, **options):
        """
        creates the appropriate route based on the input parameters.

        this method acts as a route factory and its corresponding service
        will be registered as default route factory on application startup.

        :param str rule: unique url rule to register this route for.
                         routes with duplicated urls and http methods will be
                         overwritten if `replace=True` option is provided.
                         otherwise an error will be raised.

        :keyword bool authenticated: specifies that this route could not be accessed
                                     if the requester has not been authenticated.
                                     defaults to True if not provided.

        :keyword bool fresh_auth: specifies that this route could not be accessed
                                  if the requester has not a fresh authentication.
                                  fresh authentication means an authentication that
                                  has been done by providing user credentials to server.
                                  defaults to False if not provided.

        :keyword PermissionBase | tuple[PermissionBase] permissions: all required permissions
                                                                     to access this route.

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

        :keyword bool indexed: specifies that list results must
                               include an extra field as row index.
                               the name of the index field and the initial value
                               of index could be provided by `index_name` and
                               `start_index` respectively. `indexed` keyword has
                               only effect if the returning result contains a list
                               of objects.

        :keyword str index_name: name of the extra field to contain
                                 the row index of each result. if not provided
                                 defaults to `row_num` value.

        :keyword int start_index: the initial value of row index. if not
                                  provided, starts from 1.

        :keyword SECURE_TRUE | SECURE_FALSE readable: specifies that any column or attribute
                                                      which has `allow_read=False` or its name
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

        :keyword bool paged: specifies that this route should return paginated results.
                             defaults to False if not provided.

        :keyword int page_size: default page size for this route.
                                defaults to `default_page_size` from
                                `database` config store if not provided.

        :keyword int max_page_size: maximum page size that client is allowed
                                    to request for this route. defaults to
                                    `max_page_size` from `database` configs store
                                    if not provided.

        :keyword bool cors_enabled: specifies that cross origin resource sharing is enabled.
                                    if not provided, it will be get from cors config store.

        :keyword bool cors_always_send: specifies that cors headers must be included in
                                        response even if the request does not have origin header.
                                        if not provided, it will be get from cors config store.

        :keyword list[str] cors_allowed_origins: a list of extra allowed origins to be used
                                                 in conjunction with default allowed ones.

        :keyword list[str] cors_exposed_headers: extra exposed headers to be combined
                                                 with default ones.

        :keyword list[str] cors_allowed_headers: extra allowed headers to be combined
                                                 with default ones.

        :keyword bool cors_allow_credentials: specifies that browsers are allowed to pass
                                              response headers to front-end javascript code
                                              if the route is authenticated.
                                              if not provided, it will be get from cors config
                                              store.

        :keyword int cors_max_age: maximum number of seconds to cache results.
                                   if not provided, it will be get from cors config store.

        :raises InvalidCustomRouteTypeError: invalid custom route type error.
        :raises RouteAuthenticationMismatchError: route authentication mismatch error.
        :raises PageSizeLimitError: page size limit error.
        :raises MaxContentLengthLimitMismatchError: max content length limit mismatch error.
        :raises InvalidViewFunctionTypeError: invalid view function type error.
        :raises InvalidResultSchemaTypeError: invalid result schema type error.
        :raises InvalidResponseStatusCodeError: invalid response status code error.

        :rtype: RouteBase
        """

        route = self._create_route(rule, **options)
        if route is not None:
            if not isinstance(route, RouteBase):
                route_name = misc_utils.try_get_fully_qualified_name(route)
                base_name = misc_utils.try_get_fully_qualified_name(RouteBase)
                raise InvalidCustomRouteTypeError('Custom route [{route}] is not '
                                                  'an instance of [{base}].'
                                                  .format(route=route_name, base=base_name))
            return route

        authenticated = options.get('authenticated')
        if authenticated is None:
            authenticated = True

        fresh_auth = options.get('fresh_auth')
        if fresh_auth is None:
            fresh_auth = False

        request_limit = options.get('request_limit')
        lifetime = options.get('lifetime')
        temporary = request_limit is not None or lifetime is not None

        if authenticated is False and fresh_auth is False and temporary is False:
            return PublicRoute(rule, **options)
        elif authenticated is False and fresh_auth is False and temporary is True:
            return PublicTemporaryRoute(rule, **options)
        elif authenticated is True and fresh_auth is False and temporary is False:
            return ProtectedRoute(rule, **options)
        elif authenticated is True and fresh_auth is False and temporary is True:
            return ProtectedTemporaryRoute(rule, **options)
        elif authenticated is True and fresh_auth is True and temporary is False:
            return FreshProtectedRoute(rule, **options)
        elif authenticated is True and fresh_auth is True and temporary is True:
            return FreshProtectedTemporaryRoute(rule, **options)
        else:
            raise RouteAuthenticationMismatchError('[authenticated={auth}] and '
                                                   '[fresh_auth={fresh}] and '
                                                   '[temporary={temp}] in route '
                                                   '[{route}] are incompatible.'
                                                   .format(auth=authenticated,
                                                           fresh=fresh_auth,
                                                           temp=temporary,
                                                           route=rule))

    def _create_route(self, rule, **options):
        """
        creates the appropriate route based on the input parameters.

        this method is intended to be overridden by subclasses to provided
        custom `RouteBase` types. it should always return a descendant object
         of `RouteBase` or `None`.

        :param str rule: unique url rule to register this route for.
                         routes with duplicated urls and http methods will be
                         overwritten if `replace=True` option is provided.
                         otherwise an error will be raised.

        :keyword bool authenticated: specifies that this route could not be accessed
                                     if the requester has not been authenticated.
                                     defaults to True if not provided.

        :keyword bool fresh_auth: specifies that this route could not be accessed
                                  if the requester has not a fresh authentication.
                                  fresh authentication means an authentication that
                                  has been done by providing user credentials to server.
                                  defaults to False if not provided.

        :keyword PermissionBase | tuple[PermissionBase] permissions: all required permissions
                                                                     to access this route.

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

        :keyword bool indexed: specifies that list results must
                               include an extra field as row index.
                               the name of the index field and the initial value
                               of index could be provided by `index_name` and
                               `start_index` respectively. `indexed` keyword has
                               only effect if the returning result contains a list
                               of objects.

        :keyword str index_name: name of the extra field to contain
                                 the row index of each result. if not provided
                                 defaults to `row_num` value.

        :keyword int start_index: the initial value of row index. if not
                                  provided, starts from 1.

        :keyword SECURE_TRUE | SECURE_FALSE readable: specifies that any column or attribute
                                                      which has `allow_read=False` or its name
                                                      starts with underscore `_`, should not
                                                      be included in result dict. defaults to
                                                      `SECURE_TRUE` if not provided. it will
                                                      be used only for entity conversion.
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

        :keyword bool paged: specifies that this route should return paginated results.
                             defaults to False if not provided.

        :keyword int page_size: default page size for this route.
                                defaults to `default_page_size` from
                                `database` config store if not provided.

        :keyword int max_page_size: maximum page size that client is allowed
                                    to request for this route. defaults to
                                    `max_page_size` from `database` configs store
                                    if not provided.

        :keyword bool cors_enabled: specifies that cross origin resource sharing is enabled.
                                    if not provided, it will be get from cors config store.

        :keyword bool cors_always_send: specifies that cors headers must be included in
                                        response even if the request does not have origin header.
                                        if not provided, it will be get from cors config store.

        :keyword list[str] cors_allowed_origins: a list of extra allowed origins to be used
                                                 in conjunction with default allowed ones.

        :keyword list[str] cors_exposed_headers: extra exposed headers to be combined
                                                 with default ones.

        :keyword list[str] cors_allowed_headers: extra allowed headers to be combined
                                                 with default ones.

        :keyword bool cors_allow_credentials: specifies that browsers are allowed to pass
                                              response headers to front-end javascript code
                                              if the route is authenticated.
                                              if not provided, it will be get from cors config
                                              store.

        :keyword int cors_max_age: maximum number of seconds to cache results.
                                   if not provided, it will be get from cors config store.

        :raises PageSizeLimitError: page size limit error.
        :raises MaxContentLengthLimitMismatchError: max content length limit mismatch error.
        :raises InvalidViewFunctionTypeError: invalid view function type error.
        :raises InvalidResultSchemaTypeError: invalid result schema type error.
        :raises InvalidResponseStatusCodeError: invalid response status code error.

        :rtype: RouteBase
        """

        return None

    def add_route(self, url, view_func=None,
                  provide_automatic_options=None, **options):
        """
        connects a url rule. the provided view_func will be registered with the endpoint.

        if there is another rule with the same url and http methods and `replace=True`
        option is provided, it will be replaced. otherwise an error will be raised.

        a note about endpoint. pyrin will handle endpoint generation on its own.
        so there is no endpoint parameter in this method's signature.
        this is required to be able to handle uniqueness of endpoints and managing them.
        despite flask, pyrin will not require you to define view functions with unique names.
        you could define view functions with the same name in different modules. but to
        ensure the uniqueness of endpoints, pyrin will use the fully qualified name
        of function as endpoint. for example: `pyrin.api.services.create_route`.
        so you could figure out endpoint for any view function to use it in places
        like `url_for` method.

        pyrin handles endpoints this way to achieve these two important features:

        1. dismissal of the need for view function name uniqueness.
           when application grows, it's nonsense to be forced to have
           unique view function names at application level.

        2. managing routes with the same url and http methods, and informing
           the developer about them to prevent accidental replacements. and also
           providing a way to replace a route by another route with the same url
           and http methods if that is what developer actually wants.
           when application grows, it becomes a point of failure when you have no
           idea that you've registered a similar route in multiple places and only
           one of them will be get called based on registration order.

        :param str url: the url rule as string.

        :param function view_func: the function to call when serving a request to the
                                   provided endpoint.

        :param bool provide_automatic_options: controls whether the `OPTIONS` method should be
                                               added automatically.
                                               this can also be controlled by setting the
                                               `view_func.provide_automatic_options = False`
                                               before adding the rule.

        :keyword str | tuple[str] methods: http methods that this rule should handle.
                                           if not provided, defaults to `GET`.

        :keyword PermissionBase | tuple[PermissionBase] permissions: all required permissions
                                                                     for accessing this route.

        :keyword bool authenticated: specifies that this route could not be accessed
                                     if the requester has not been authenticated.
                                     defaults to True if not provided.

        :keyword bool fresh_auth: specifies that this route could not be accessed
                                  if the requester has not a fresh authentication.
                                  fresh authentication means an authentication that
                                  has been done by providing user credentials to
                                  server. defaults to False if not provided.

        :keyword bool replace: specifies that this route must replace any existing
                               route with the same url and http methods or raise
                               an error if not provided. defaults to False.

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

        :keyword str | list[str] environments: a list of all environments that this
                                               route must be exposed on them.
                                               the values could be from all available
                                               environments in environments config store.
                                               for example: `production`, `development`.
                                               if not provided, the route will be exposed
                                               on all environments.

        :keyword ResultSchema result_schema: result schema to be used to filter results.

        :keyword bool indexed: specifies that list results must
                               include an extra field as row index.
                               the name of the index field and the initial value
                               of index could be provided by `index_name` and
                               `start_index` respectively. `indexed` keyword has
                               only effect if the returning result contains a list
                               of objects.

        :keyword str index_name: name of the extra field to contain
                                 the row index of each result. if not provided
                                 defaults to `row_num` value.

        :keyword int start_index: the initial value of row index. if not
                                  provided, starts from 1.

        :keyword SECURE_TRUE | SECURE_FALSE readable: specifies that any column or attribute
                                                      which has `allow_read=False` or its name
                                                      starts with underscore `_`, should not
                                                      be included in result dict. defaults
                                                      to `SECURE_TRUE` if not provided.
                                                      it will be used only for entity
                                                      conversion. this value will override
                                                      the corresponding value of
                                                      `result_schema` if provided.

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

        :keyword bool paged: specifies that this route should return paginated results.
                             defaults to False if not provided.

        :keyword int page_size: default page size for this route.
                                defaults to `default_page_size` from
                                `database` config store if not provided.

        :keyword int max_page_size: maximum page size that client is allowed
                                    to request for this route. defaults to
                                    `max_page_size` from `database` configs store
                                    if not provided.

        :keyword bool cors_enabled: specifies that cross origin resource sharing is enabled.
                                    if not provided, it will be get from cors config store.

        :keyword bool cors_always_send: specifies that cors headers must be included in
                                        response even if the request does not have origin header.
                                        if not provided, it will be get from cors config store.

        :keyword list[str] cors_allowed_origins: a list of extra allowed origins to be used
                                                 in conjunction with default allowed ones.

        :keyword list[str] cors_exposed_headers: extra exposed headers to be combined
                                                 with default ones.

        :keyword list[str] cors_allowed_headers: extra allowed headers to be combined
                                                 with default ones.

        :keyword bool cors_allow_credentials: specifies that browsers are allowed to pass
                                              response headers to front-end javascript code
                                              if the route is authenticated.
                                              if not provided, it will be get from cors config
                                              store.

        :keyword int cors_max_age: maximum number of seconds to cache results.
                                   if not provided, it will be get from cors config store.

        :raises DuplicateRouteURLError: duplicate route url error.
        :raises OverwritingEndpointIsNotAllowedError: overwriting endpoint is not allowed error.
        :raises PageSizeLimitError: page size limit error.
        :raises MaxContentLengthLimitMismatchError: max content length limit mismatch error.
        :raises InvalidViewFunctionTypeError: invalid view function type error.
        :raises InvalidResultSchemaTypeError: invalid result schema type error.
        :raises InvalidResponseStatusCodeError: invalid response status code error.
        """

        application_services.add_url_rule(url, view_func=view_func,
                                          provide_automatic_options=provide_automatic_options,
                                          **options)

# -*- coding: utf-8 -*-
"""
router handlers base module.
"""

import time

from threading import Lock

from werkzeug.routing import Rule

import pyrin.processor.response.services as response_services
import pyrin.processor.response.status.services as status_services
import pyrin.configuration.services as config_services
import pyrin.security.session.services as session_services
import pyrin.utils.misc as misc_utils
import pyrin.utils.headers as header_utils
import pyrin.utils.function as func_utils

from pyrin.core.globals import _
from pyrin.processor.cors.structs import CORS
from pyrin.api.schema.structs import ResultSchema
from pyrin.core.enumerations import HTTPMethodEnum
from pyrin.database.paging.paginator import SimplePaginator
from pyrin.processor.response.wrappers.base import CoreResponse
from pyrin.processor.response.enumerations import ResponseHeaderEnum
from pyrin.api.router.handlers.exceptions import InvalidViewFunctionTypeError, \
    MaxContentLengthLimitMismatchError, InvalidResultSchemaTypeError, \
    RouteIsNotBoundedToMapError, RouteIsNotBoundedError, InvalidResponseStatusCodeError, \
    RequestLimitOrLifetimeRequiredError, InvalidRequestLimitError, \
    InvalidLifetimeError, URLNotFoundError, ViewFunctionRequiredParamsError


class RouteBase(Rule):
    """
    route base class.

    this class should be used as base for all route types.
    """

    # these are http methods that will not be considered as operational.
    NON_OPERATIONAL_METHODS = [HTTPMethodEnum.HEAD,
                               HTTPMethodEnum.OPTIONS]

    result_schema_class = ResultSchema
    paginator_class = SimplePaginator
    cors_class = CORS

    def __init__(self, rule, **options):
        """
        initializes an instance of RouteBase.

        :param str rule: unique url rule to register this route for.
                         routes with duplicated urls and http methods will be
                         overwritten if `replace=True` option is provided.
                         otherwise an error will be raised.

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

        :keyword ResultSchema | type[ResultSchema] result_schema: result schema to be used
                                                                  to filter results. it could
                                                                  be an instance or a type
                                                                  of `ResultSchema` class.

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
        """

        methods = options.get('methods', None)
        methods = misc_utils.make_iterable(methods, tuple)
        options.update(methods=methods)

        self._namespace = config_services.get('api', 'general', 'namespace', default=None)
        if self._namespace not in (None, '') and not self._namespace.isspace():
            rule = '{namespace}{rule}'.format(namespace=self._namespace, rule=rule)

        append_slash = config_services.get('api', 'general', 'append_slash', default=True)
        if not rule.endswith('/') and append_slash is True:
            rule = '{rule}/'.format(rule=rule)

        # we should call super method with exact param names because it
        # does not have `**options` in it's signature and raises an error
        # if extra keywords passed to it.
        super().__init__(rule,
                         defaults=options.get('defaults', None),
                         subdomain=options.get('subdomain', None),
                         methods=methods,
                         build_only=options.get('build_only', False),
                         endpoint=options.get('endpoint', None),
                         strict_slashes=options.get('strict_slashes', None),
                         merge_slashes=options.get('merge_slashes', None),
                         redirect_to=options.get('redirect_to', None),
                         alias=options.get('alias', False),
                         host=options.get('host', None),
                         websocket=options.get('websocket', False))

        self._view_function = options.get('view_function')
        self._paginator = self._get_paginator(**options)
        self._result_schema = self._extract_schema(**options)
        self._cors = self._get_cors_configs(**options)

        global_limit = config_services.get('api', 'general', 'max_content_length')
        restricted_length = options.get('max_content_length',
                                        config_services.get('api',
                                                            'general',
                                                            'restricted_max_content_length'))
        if restricted_length > global_limit:
            raise MaxContentLengthLimitMismatchError('Specified max content length '
                                                     '[{restricted}] for route [{route}] is '
                                                     'higher than global limit which is '
                                                     '[{global_limit}].'
                                                     .format(restricted=restricted_length,
                                                             route=self.rule,
                                                             global_limit=global_limit))

        self._max_content_length = restricted_length

        full_name = misc_utils.try_get_fully_qualified_name(self._view_function)
        if not callable(self._view_function):
            raise InvalidViewFunctionTypeError('The provided view function [{function}] '
                                               'for route with url [{url}] is not callable.'
                                               .format(function=full_name,
                                                       url=self.rule))

        self._required_arguments = func_utils.get_required_arguments(self._view_function)
        self._no_cache = options.get('no_cache', False)

        status_code = options.pop('status_code', None)
        if status_code is not None and \
                status_services.is_processed(status_code, **options) is not True:
            raise InvalidResponseStatusCodeError('The provided status code [{status}] for '
                                                 'route [{route}] on view function [{function}] '
                                                 'must be from information, success or '
                                                 'redirection codes. and if you want to return '
                                                 'a status code for errors, you should raise '
                                                 'an exception with relevant code as status '
                                                 'code inside your method. pyrin will handle '
                                                 'exceptions and converts them to correct '
                                                 'responses.'
                                                 .format(status=status_code,
                                                         route=self.rule,
                                                         function=full_name))
        self._status_code = status_code

    def __eq__(self, other):
        """
        gets a value indicating that current route is equal to provided route.

        note that for two routes to be considered equal, three conditions must be met:

        1. both routes be an instance of `RouteBase`.
        2. both routes have the same exact url rule.
        3. both routes have the same exact http methods.

        this has some differences with how flask compares routes.
        and this is required because pyrin handles routes on its own and assures
        that there should not be multiple routes with the same url and http methods.

        :param object other: other instance to be compared to current route.

        :rtype: bool
        """

        if not isinstance(other, RouteBase):
            return False

        return self._trace == other._trace and \
            sorted(set(self.methods)) == sorted(set(other.methods))

    def unbind(self, map):
        """
        sets this route's map to None.

        :param Map map: the map that this route is bounded to.
                        it must be the exact map of this route.

        :raises RouteIsNotBoundedError: route is not bounded error.
        :raises RouteIsNotBoundedToMapError: route is not bounded to map error.
        """

        if self.map is None:
            raise RouteIsNotBoundedError('Route [{route}] is not bounded to any Map.'
                                         .format(route=self))

        if self.map is not map:
            raise RouteIsNotBoundedToMapError('Route [{route}] is not bounded '
                                              'to provided Map [{map}].'
                                              .format(route=self, map=map))

        self.map = None

    def get_duplicate_methods(self, methods):
        """
        gets a tuple of this route's methods that are duplicated with provided methods.

        it gets an empty tuple if no duplication found.
        note that any of `NON_OPERATIONAL_METHODS` will not be considered
        for duplication. because these two methods will be handled correctly by
        flask itself. but if you want to explicitly define routes for these type
        of methods, you have to implement the required parts manually.

        :param str | tuple[str] methods: http methods to check for duplication.

        :returns: tuple of duplicate methods.
        :rtype: tuple[str]
        """

        methods = misc_utils.make_iterable(methods, set)
        duplicate_methods = set(self.methods).intersection(methods)
        duplicate_methods = duplicate_methods.difference(set(self.NON_OPERATIONAL_METHODS))

        return tuple(duplicate_methods)

    def remove_methods(self, methods):
        """
        removes the provided methods from this route's methods.

        note that this will not remove any of `NON_OPERATIONAL_METHODS`.

        :param str | tuple[str] methods: http methods to be removed.
        """

        to_be_removed = self.get_duplicate_methods(methods)
        updated_methods = set(self.methods).difference(set(to_be_removed))
        self.methods = updated_methods
        self.refresh()

    def handle(self, inputs, **options):
        """
        handles the current route.

        :param dict inputs: view function inputs.

        :raises ViewFunctionRequiredParamsError: view function required params error.

        :returns: view function's result.
        :rtype: object
        """

        if self._result_schema is not None:
            self._inject_result_schema()

        if self._paginator is not None:
            self._inject_paginator(inputs, **options)

        self._handle(inputs, **options)
        result = self._call_view_function(inputs, **options)
        self._finished(result, **options)

        return self._prepare_response(result)

    def _get_paginator(self, **options):
        """
        gets paginator for this route if required.

        :keyword bool paged: specifies that this route should return paginated results.
                             defaults to False if not provided.

        :keyword int page_size: default page size for this route.
                                defaults to `default_page_size` from
                                `database` config store if not provided.

        :keyword int max_page_size: maximum page size that client is allowed
                                    to request for this route. defaults to
                                    `max_page_size` from `database` configs store
                                    if not provided.

        :raises PageSizeLimitError: page size limit error.

        :rtype: PaginatorBase
        """

        paged = options.get('paged', False)
        if paged is True:
            return self.paginator_class(**options)

        return None

    def _get_cors_configs(self, **options):
        """
        gets cors configs for this route if enabled.

        :keyword bool cors_enabled: specifies that cross origin resource sharing is enabled.
                                    defaults to False if not provided.

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
        """

        return self.cors_class(**options)

    def _handle(self, inputs, **options):
        """
        handles the current route.

        routes which need to perform extra operations before
        view function execution, must override this method.

        :param dict inputs: view function inputs.
        """
        pass

    def _finished(self, result, **options):
        """
        does the extra required works after the view function has been executed.

        routes which need to perform extra operations after
        view function execution, must override this method.

        :param object result: view function execution result.
        """
        pass

    def _extract_schema(self, **options):
        """
        extracts schema related attributes from given values and returns an schema object.

        if no schema related item is provided, it returns None.

        :keyword ResultSchema | type[ResultSchema] result_schema: result schema to be used
                                                                  to filter results. it could
                                                                  be an instance or a type
                                                                  of `ResultSchema` class.

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

        :raises InvalidResultSchemaTypeError: invalid result schema type error.

        :rtype: ResultSchema
        """

        result_schema = options.get('result_schema')
        is_subclass = isinstance(result_schema, type) and issubclass(result_schema, ResultSchema)
        is_instance = isinstance(result_schema, ResultSchema)
        if result_schema is not None and not is_instance and not is_subclass:
            raise InvalidResultSchemaTypeError('Input parameter [{instance}] is not '
                                               'an instance or subclass of [{base}].'
                                               .format(instance=result_schema,
                                                       base=ResultSchema))

        readable = options.get('readable')
        depth = options.get('depth')
        indexed = options.get('indexed')
        index_name = options.get('index_name')
        start_index = options.get('start_index')

        if result_schema is not None and is_subclass:
            result_schema = result_schema()

        if result_schema is None and (readable is not None or
                                      depth is not None or indexed is True):
            return self.result_schema_class(readable=readable, depth=depth,
                                            indexed=indexed, index_name=index_name,
                                            start_index=start_index)

        elif result_schema is not None and (readable is not None or depth is not None or
                                            indexed is not None or index_name is not None or
                                            start_index is not None):
            updated_schema = result_schema.copy()
            if readable is not None:
                updated_schema.readable = readable
            if depth is not None:
                updated_schema.depth = depth
            if indexed is not None:
                updated_schema.indexed = indexed
            if index_name is not None:
                updated_schema.index_name = index_name
            if start_index is not None:
                updated_schema.start_index = start_index

            return updated_schema

        return result_schema

    def _prepare_response(self, response):
        """
        prepares given response to be returned to client.

        it does some operations such as adding this route's status code
        into response. if the response from view function already is a
        tuple with status code, then the status code of this route
        won't be injected.

        :param object | tuple | dict | CoreResponse response: response value to be prepared.

        :note response: it could be an object or a dict or a tuple with the length of 2 or 3.
                        in the form of: body
                                        body, status_code
                                        body, headers
                                        body, status_code, header

        :rtype: tuple[object, int, dict | Headers] | object
        """

        body, status_code, headers = response_services.unpack_response(response)
        if status_code is None and self.status_code is not None:
            status_code = self.status_code
        elif status_code is None and self.status_code is None:
            status_code = status_services.get_status_code()

        headers = self._prepare_headers(headers)
        return response_services.pack_response(body, status_code, headers)

    def _prepare_headers(self, headers):
        """
        prepares required headers into given dict.

        :param dict | Headers headers: headers dict to be prepared.

        :rtype: CoreHeaders
        """

        if self._no_cache is True:
            headers = header_utils.convert_headers(headers, ignore_null=False)
            cache_header = {ResponseHeaderEnum.CACHE_CONTROL: 'no-cache'}
            headers.extend(cache_header)

        return headers

    def _inject_result_schema(self):
        """
        injects this route's result schema into current request context.
        """

        session_services.add_request_context('result_schema', self._result_schema)

    def _inject_paginator(self, inputs, **options):
        """
        injects this route's paginator into current request context.

        :param dict inputs: view function inputs.
        """

        paginator = self._paginator.copy()
        request = session_services.get_current_request()
        paging_params = request.get_paging_params()
        paginator.inject_paging_keys(inputs, **paging_params)
        session_services.add_request_context('paginator', paginator)

    def _call_view_function(self, inputs, **options):
        """
        calls the route's view function.

        :param dict inputs: view function inputs.

        :raises ViewFunctionRequiredParamsError: view function required params error.

        :returns: view function's result.
        :rtype: object
        """

        self._check_required_arguments(inputs)
        return self.view_function(**inputs)

    def _check_required_arguments(self, inputs):
        """
        checks that all required arguments for this route are present in inputs.

        :raises ViewFunctionRequiredParamsError: view function required params error.
        """

        not_present = self._required_arguments.difference(set(inputs.keys()))
        present = self._required_arguments.difference(not_present)
        not_present = list(not_present)

        for item in present:
            if inputs.get(item) is None:
                not_present.append(item)

        if len(not_present) > 0:
            raise ViewFunctionRequiredParamsError(_('These values are required: {params}')
                                                  .format(params=not_present))

    @property
    def view_function(self):
        """
        gets this route's view function.

        :rtype: callable
        """

        return self._view_function

    @property
    def required_arguments(self):
        """
        gets this route's required arguments.

        :rtype: set[str]
        """

        return self._required_arguments

    @property
    def max_content_length(self):
        """
        gets this route's max content length in bytes.

        :rtype: int
        """

        return self._max_content_length

    @property
    def result_schema(self):
        """
        gets this route's result schema if available.

        :rtype: ResultSchema
        """

        return self._result_schema

    @property
    def is_operational(self):
        """
        gets a value indicating that this route has any operational http methods.

        note that any of `NON_OPERATIONAL_METHODS` will not be considered as operational.

        :rtype: bool
        """

        operational_methods = set(self.methods).difference(set(self.NON_OPERATIONAL_METHODS))
        return len(operational_methods) > 0

    @property
    def status_code(self):
        """
        gets this route's success response status code.

        it could be None if not provided.

        :rtype: int
        """

        return self._status_code

    @property
    def cors(self):
        """
        gets cors attribute of this route.

        :rtype: CORS
        """

        return self._cors


class TemporaryRouteBase(RouteBase):
    """
    temporary route bass class.

    this class should be used as base for all temporary route types.
    this type of routes will unregister themselves after a number of requests
    or a period of time after registration.
    """

    def __init__(self, rule, **options):
        """
        initializes an instance of TemporaryRouteBase.

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

        :keyword ResultSchema | type[ResultSchema] result_schema: result schema to be used
                                                                  to filter results. it could
                                                                  be an instance or a type
                                                                  of `ResultSchema` class.

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

        # the threading lock must be separated for each instance.
        # because each route will have its own unique instance during application runtime.
        self._lock = Lock()

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
        increases performed requests count of this route by one.
        """

        with self._lock:
            self._total_requests = self._total_requests + 1

    def _handle(self, inputs, **options):
        """
        handles the current route.

        :param dict inputs: view function inputs.

        :raises URLNotFoundError: url not found error.
        """

        if self._should_unregister() is True:
            self._unregister()
            raise URLNotFoundError(_('The requested URL was not found on the server. If you '
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

        self.map.remove(self)

# -*- coding: utf-8 -*-
"""
router handlers protected module.
"""

import pyrin.security.authorization.services as authorization_services
import pyrin.security.session.services as session_services
import pyrin.utils.misc as misc_utils

from pyrin.core.globals import _
from pyrin.api.router.handlers.base import RouteBase, TemporaryRouteBase
from pyrin.processor.request.enumerations import RequestHeaderEnum
from pyrin.security.permission.base import PermissionBase
from pyrin.api.router.handlers.exceptions import FreshAuthenticationRequiredError, \
    PermissionTypeError


class ProtectedRoute(RouteBase):
    """
    protected route class.

    this class should be used to manage application protected api
    routes that require authenticated access.
    """

    def __init__(self, rule, **options):
        """
        initializes an instance of ProtectedRoute.

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
                                                      be included in result dict. defaults to
                                                      `SECURE_TRUE` if not provided. it will
                                                      be used only for entity conversion. this
                                                      value will override the corresponding
                                                      value of `result_schema` if provided.

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

        :keyword PermissionBase | tuple[PermissionBase] permissions: all required permissions
                                                                     to access this route.

        :raises PageSizeLimitError: page size limit error.
        :raises MaxContentLengthLimitMismatchError: max content length limit mismatch error.
        :raises InvalidViewFunctionTypeError: invalid view function type error.
        :raises InvalidResultSchemaTypeError: invalid result schema type error.
        :raises InvalidResponseStatusCodeError: invalid response status code error.
        :raises PermissionTypeError: permission type error.
        """

        super().__init__(rule, **options)

        if self._cors is not None:
            self._cors.add_allowed_headers(RequestHeaderEnum.AUTHORIZATION)

        self._permissions = options.get('permissions', None)
        self._permissions = misc_utils.make_iterable(self._permissions, tuple)

        if not all(isinstance(item, PermissionBase) for item in self._permissions):
            raise PermissionTypeError('All route permissions must be an '
                                      'instance of [{instance}].'
                                      .format(instance=PermissionBase))

    def _handle(self, inputs, **options):
        """
        handles the current route.

        routes which need to perform extra operations before
        view function execution, must override this method.

        :param dict inputs: view function inputs.

        :raises UserNotAuthenticatedError: user not authenticated error.
        :raises UserIsNotActiveError: user is not active error.
        :raises AuthorizationFailedError: authorization failed error.
        """

        self._authorize()
        super()._handle(inputs, **options)

    def _authorize(self):
        """
        authorizes the route permissions for current user.

        :raises UserNotAuthenticatedError: user not authenticated error.
        :raises UserIsNotActiveError: user is not active error.
        :raises AuthorizationFailedError: authorization failed error.
        """

        user = session_services.get_current_user()
        authorization_services.authorize(user, self.permissions)

    @property
    def permissions(self):
        """
        gets all required permissions to access this route.

        :returns: tuple[PermissionBase]

        :rtype: tuple
        """

        return self._permissions


class FreshProtectedRoute(ProtectedRoute):
    """
    fresh protected route class.

    this class should be used to manage application protected api routes that
    require fresh authenticated access. fresh authentication means an authentication
    that has been done by providing user credentials to server.
    """

    def _authorize(self):
        """
        authorizes the route permissions for current user.

        also checks that the user has a fresh authentication.

        :raises FreshAuthenticationRequiredError: fresh authentication required error.
        :raises UserNotAuthenticatedError: user not authenticated error.
        :raises UserIsNotActiveError: user is not active error.
        :raises AuthorizationFailedError: authorization failed error.
        """

        if not session_services.is_fresh():
            raise FreshAuthenticationRequiredError(_('Fresh authentication is required '
                                                     'to access the requested resource.'))

        super()._authorize()


class ProtectedTemporaryRoute(ProtectedRoute, TemporaryRouteBase):
    """
    protected temporary route class.

    this class should be used to manage application protected api
    routes that require authenticated access and must be unregistered
    after a specified number of requests or a duration of time.
    this is useful for a couple of different things but mostly for system
    health checking after each new deployment on production.
    """
    pass


class FreshProtectedTemporaryRoute(FreshProtectedRoute, TemporaryRouteBase):
    """
    fresh protected temporary route class.

    this class should be used to manage application protected api routes
    that require fresh authenticated access and must be unregistered
    after a specified number of requests or a duration of time.
    this is useful for a couple of different things but mostly for system
    health checking after each new deployment on production.
    """
    pass

# -*- coding: utf-8 -*-
"""
cors manager module.
"""

from werkzeug.exceptions import HTTPException

import pyrin.application.services as application_services
import pyrin.security.session.services as session_services
import pyrin.configuration.services as config_services
import pyrin.utils.string as string_utils

from pyrin.processor.cors import CORSPackage
from pyrin.core.structs import Manager, CoreHeaders
from pyrin.processor.cors.enumerations import CORSResponseHeaderEnum, CORSRequestHeaderEnum
from pyrin.processor.request.enumerations import RequestHeaderEnum
from pyrin.processor.response.enumerations import ResponseHeaderEnum


class CORSManager(Manager):
    """
    cors manager class.
    """

    package_class = CORSPackage
    WILDCARD = '*'

    def __init__(self):
        """
        initializes an instance of CORSManager.
        """

        super().__init__()

        self._enabled = config_services.get_active('cors', 'enable')
        self._always_send = config_services.get_active('cors', 'always_send')
        self._allowed_origins = set(config_services.get_active('cors', 'allowed_origins') or [])
        self._allowed_headers = set(config_services.get_active('cors', 'allowed_headers') or [])
        self._exposed_headers = set(config_services.get_active('cors', 'exposed_headers') or [])
        self._allow_credentials = config_services.get_active('cors', 'allow_credentials')
        self._max_age = config_services.get_active('cors', 'max_age')

    def _validate_credentials(self, items, **options):
        """
        validates that if credentials are supported or not.

        if credentials are supported, it removes `*` from values in the given list.

        :param list[str] | set[str] items: items to be validated.

        :keyword bool allow_credentials: specifies that browsers are allowed to pass
                                         response headers to front-end javascript code
                                         if the route is authenticated.
                                         if not provided, defaults to `_allow_credentials`
                                         attribute value.
        """

        if self._should_allow_credentials(**options) is not False:
            if self.WILDCARD in items:
                items.remove(self.WILDCARD)

    def _is_enabled(self, **options):
        """
        gets a value indicating that cors headers must be sent in response.

        :keyword bool enabled: specifies that cors headers must be sent in response.
                               if not provided, defaults to `_enabled` attribute value.

        :rtype: bool
        """

        enabled = options.get('enabled')
        if enabled is None:
            enabled = self._enabled

        return enabled

    def _should_always_send(self, **options):
        """
        gets a value indicating that cors headers must be included in response
        even if the request does not have origin header.

        :keyword bool always_send: specifies that cors headers must be included in
                                   response even if the request does not have origin header.
                                   if not provided, defaults to `_always_send` attribute value.
        :rtype: bool
        """

        always_send = options.get('always_send')
        if always_send is None:
            always_send = self._always_send

        return always_send

    def _should_allow_credentials(self, **options):
        """
        gets a value indicating that browsers are allowed to pass response
        headers to front-end javascript code if the route is authenticated.

        :keyword bool allow_credentials: specifies that browsers are allowed to pass
                                         response headers to front-end javascript code
                                         if the route is authenticated.
                                         if not provided, defaults to `_allow_credentials`
                                         attribute value.

        :rtype: bool
        """

        allow_credentials = options.get('allow_credentials')
        if allow_credentials is None:
            allow_credentials = self._allow_credentials

        return allow_credentials

    def _get_allowed_origins(self, **options):
        """
        gets all allowed origins combining default and extra ones.

        :keyword list[str] allowed_origins: extra allowed origins to be combined
                                            with default ones.

        :keyword bool allow_credentials: specifies that browsers are allowed to pass
                                         response headers to front-end javascript code
                                         if the route is authenticated.
                                         if not provided, defaults to `_allow_credentials`
                                         attribute value.

        :rtype: set[str]
        """

        allowed_origins = options.get('allowed_origins') or []
        allowed_origins = set(allowed_origins).union(self._allowed_origins)
        self._validate_credentials(allowed_origins, **options)
        return allowed_origins

    def _get_allowed_headers(self, **options):
        """
        gets all allowed request headers combining default and extra ones.

        :keyword list[str] allowed_headers: extra allowed headers to be combined
                                            with default ones.

        :keyword bool allow_credentials: specifies that browsers are allowed to pass
                                         response headers to front-end javascript code
                                         if the route is authenticated.
                                         if not provided, defaults to `_allow_credentials`
                                         attribute value.

        :rtype: set[str]
        """

        allowed_headers = options.get('allowed_headers') or []
        allowed_headers = set(allowed_headers).union(self._allowed_headers)
        self._validate_credentials(allowed_headers, **options)
        return allowed_headers

    def _get_exposed_headers(self, **options):
        """
        gets all exposed response headers combining default and extra ones.

        :keyword list[str] exposed_headers: extra exposed headers to be combined
                                            with default ones.

        :keyword bool allow_credentials: specifies that browsers are allowed to pass
                                         response headers to front-end javascript code
                                         if the route is authenticated.
                                         if not provided, defaults to `_allow_credentials`
                                         attribute value.

        :rtype: list[str]
        """

        exposed_headers = options.get('exposed_headers') or []
        exposed_headers = sorted(set(exposed_headers).union(self._exposed_headers))
        self._validate_credentials(exposed_headers, **options)
        return exposed_headers

    def _get_max_age(self, **options):
        """
        gets the max age for cors enabled routes to be cached in seconds.

        it returns None if no max age is set.

        :keyword int max_age: maximum number of seconds to cache results.
                              if not provided, defaults to `_max_age` attribute value.

        :rtype: int
        """

        return options.setdefault('max_age', self._max_age)

    def _get_response_origin(self, origin, **options):
        """
        gets the origin to be set in response header.

        it returns None if conditions are not met.

        :param str origin: the origin name from request.

        :keyword bool allow_credentials: specifies that browsers are allowed to pass
                                         response headers to front-end javascript code
                                         if the route is authenticated.
                                         if not provided, defaults to `_allow_credentials`
                                         attribute value.

        :keyword list[str] allowed_origins: a list of extra allowed origins to be used
                                            in conjunction with default allowed ones.

        :rtype: str
        """

        allowed_origins = self._get_allowed_origins(**options)
        if origin not in (None, '', self.WILDCARD):
            if string_utils.is_match(origin, allowed_origins) is True:
                return origin

            if self.WILDCARD in allowed_origins:
                return self.WILDCARD

        elif self._should_always_send(**options) is True and \
                self.WILDCARD in allowed_origins:
            return self.WILDCARD

        return None

    def _get_response_allowed_headers(self, headers, **options):
        """
        gets those requested headers which are allowed for cors enabled routes.

        :param list[str] headers: list of requested headers to be checked if are allowed.

        :keyword list[str] allowed_headers: extra allowed headers to be combined
                                            with default ones.

        :keyword bool allow_credentials: specifies that browsers are allowed to pass
                                         response headers to front-end javascript code
                                         if the route is authenticated.
                                         if not provided, defaults to `_allow_credentials`
                                         attribute value.

        :rtype: list[str]
        """

        allowed_headers = self._get_allowed_headers(**options)
        matching_headers = string_utils.union(headers, allowed_headers, collection=set)
        if self.WILDCARD in allowed_headers:
            matching_headers.add(self.WILDCARD)

        return sorted(matching_headers)

    def _get_common_headers(self, **options):
        """
        gets all headers that are common between preflight and actual requests.

        it returns None if cors is not enabled or request's origin is not valid.

        :keyword bool enabled: specifies that cors headers must be sent in response.
                               if not provided, defaults to `_enabled` attribute value.

        :keyword bool always_send: specifies that cors headers must be included in
                                   response even if the request does not have origin header.
                                   if not provided, defaults to `_always_send` attribute value.

        :keyword list[str] allowed_origins: a list of extra allowed origins to be used
                                            in conjunction with default allowed ones.

        :keyword bool allow_credentials: specifies that browsers are allowed to pass
                                         response headers to front-end javascript code
                                         if the route is authenticated.
                                         if not provided, defaults to `_allow_credentials`
                                         attribute value.

        :rtype: CoreHeaders
        """

        if self._is_enabled(**options) is not True:
            return None

        request = session_services.get_current_request()
        origin = self._get_response_origin(request.origin, **options)

        # if origin is not provided in request header and also wildcard
        # condition is not met, cors headers will not be added.
        if origin is None:
            return None

        headers = CoreHeaders()
        headers[CORSResponseHeaderEnum.ACCESS_CONTROL_ALLOW_ORIGIN] = origin

        vary_headers = [CORSRequestHeaderEnum.ACCESS_CONTROL_REQUEST_METHOD]
        if origin != self.WILDCARD:
            vary_headers.append(RequestHeaderEnum.ORIGIN)

        vary_headers = ', '.join(vary_headers)
        headers.add(ResponseHeaderEnum.VARY, vary_headers)

        if self._should_allow_credentials(**options) is True:
            headers[CORSResponseHeaderEnum.ACCESS_CONTROL_ALLOW_CREDENTIALS] = 'true'

        return headers

    def get_cors_headers(self, **options):
        """
        gets all headers to set in response for cors enabled actual requests.

        it returns None if cors is not enabled or request's origin is not valid.

        :keyword bool enabled: specifies that cors headers must be sent in response.
                               if not provided, defaults to `_enabled` attribute value.

        :keyword bool always_send: specifies that cors headers must be included in
                                   response even if the request does not have origin header.
                                   if not provided, defaults to `_always_send` attribute value.

        :keyword list[str] allowed_origins: a list of extra allowed origins to be used
                                            in conjunction with default allowed ones.

        :keyword list[str] exposed_headers: extra exposed headers to be combined
                                            with default ones.

        :keyword bool allow_credentials: specifies that browsers are allowed to pass
                                         response headers to front-end javascript code
                                         if the route is authenticated.
                                         if not provided, defaults to `_allow_credentials`
                                         attribute value.

        :rtype: CoreHeaders
        """

        headers = self._get_common_headers(**options)
        if headers is None:
            return None

        exposed_headers = self._get_exposed_headers(**options)
        if len(exposed_headers) > 0:
            exposed_headers = ', '.join(exposed_headers)
            headers[CORSResponseHeaderEnum.ACCESS_CONTROL_EXPOSE_HEADERS] = exposed_headers

        return headers

    def get_preflight_headers(self, *allowed_methods, **options):
        """
        gets all headers to set in response for cors preflight requests.

        it returns None if cors is not enabled or request's origin is not valid.

        :param str allowed_methods: all allowed http methods.

        :keyword bool enabled: specifies that cors headers must be sent in response.
                               if not provided, defaults to `_enabled` attribute value.

        :keyword bool always_send: specifies that cors headers must be included in
                                   response even if the request does not have origin header.
                                   if not provided, defaults to `_always_send` attribute value.

        :keyword list[str] allowed_origins: a list of extra allowed origins to be used
                                            in conjunction with default allowed ones.

        :keyword list[str] allowed_headers: extra allowed headers to be combined
                                            with default ones.

        :keyword bool allow_credentials: specifies that browsers are allowed to pass
                                         response headers to front-end javascript code
                                         if the route is authenticated.
                                         if not provided, defaults to `_allow_credentials`
                                         attribute value.

        :keyword int max_age: maximum number of seconds to cache results.
                              if not provided, defaults to `_max_age` attribute value.

        :rtype: CoreHeaders
        """

        headers = self._get_common_headers(**options)
        if headers is None:
            return None

        # if there is no 'Access-Control-Request-Method' in request headers or if it
        # does not match any of allowed methods, do not add other preflight headers.
        request = session_services.get_current_request()
        if request.access_control_request_method in (None, '') or \
                string_utils.is_match(request.access_control_request_method,
                                      allowed_methods) is False:
            return headers

        allowed_methods = ', '.join(sorted([item.upper() for item in allowed_methods]))
        headers[CORSResponseHeaderEnum.ACCESS_CONTROL_ALLOW_METHODS] = allowed_methods

        requested_headers = []
        if request.access_control_request_headers not in (None, ''):
            requested_headers = \
                request.access_control_request_headers.as_set(preserve_casing=True)

        allowed_headers = self._get_response_allowed_headers(requested_headers, **options)
        if len(allowed_headers) > 0:
            allowed_headers = ', '.join(allowed_headers)
            headers[CORSResponseHeaderEnum.ACCESS_CONTROL_ALLOW_HEADERS] = allowed_headers

        max_age = self._get_max_age(**options)
        if max_age is not None:
            headers[CORSResponseHeaderEnum.ACCESS_CONTROL_MAX_AGE] = max_age

        return headers

    def process_inputs(self, cors, **options):
        """
        processes given cors object and gets the relevant inputs as a dict.

        if any of cors objects attributes are None, it gets their values from default configs.

        :param CORS cors: cors object.

        :returns: dict(bool enabled,
                       bool always_send,
                       list[str] allowed_origins,
                       list[str] allowed_headers,
                       list[str] exposed_headers,
                       bool allow_credentials,
                       int max_age)

        :rtype: dict
        """

        enabled = cors.enabled
        always_send = cors.always_send
        allowed_origins = cors.allowed_origins
        allowed_headers = cors.allowed_headers
        exposed_headers = cors.exposed_headers
        allow_credentials = cors.allow_credentials
        max_age = cors.max_age

        if enabled is None:
            enabled = self._enabled

        if always_send is None:
            always_send = self._always_send

        if allowed_origins is None:
            allowed_origins = self._allowed_origins

        if allowed_headers is None:
            allowed_headers = self._allowed_headers

        if exposed_headers is None:
            exposed_headers = self._exposed_headers

        if allow_credentials is None:
            allow_credentials = self._allow_credentials

        if max_age is None:
            max_age = self._max_age

        return dict(enabled=enabled,
                    always_send=always_send,
                    allowed_origins=allowed_origins,
                    allowed_headers=allowed_headers,
                    exposed_headers=exposed_headers,
                    allow_credentials=allow_credentials,
                    max_age=max_age)

    def get_required_cors_headers(self):
        """
        gets cors headers for current request if required.

        if cors conditions are not met, it returns None.

        :rtype: CoreHeaders
        """

        request = session_services.get_current_request()
        if request.url_rule is not None:
            inputs = self.process_inputs(request.url_rule.cors)
            return self.get_cors_headers(**inputs)

        return None

    def get_required_preflight_headers(self):
        """
        gets preflight headers for current request if required.

        if any errors occurs or cors conditions are not met, it returns None.

        :rtype: CoreHeaders
        """

        request = session_services.get_current_request()
        adapter = application_services.get_current_url_adapter()
        headers = None
        try:
            rule, arguments = adapter.match(method=request.access_control_request_method,
                                            return_rule=True)

            inputs = self.process_inputs(rule.cors)
            headers = self.get_preflight_headers(request.access_control_request_method,
                                                 **inputs)

        except HTTPException:
            pass

        return headers

    def get_current_cors_headers(self):
        """
        gets all required cors or preflight headers.

        it may return None if cors conditions are not met.

        :rtype: CoreHeaders
        """

        request = session_services.get_current_request()
        if request.is_preflight is True:
            return self.get_required_preflight_headers()

        elif request.is_cors is True:
            return self.get_required_cors_headers()

        return None

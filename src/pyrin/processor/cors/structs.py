# -*- coding: utf-8 -*-
"""
cors structs module.
"""

import pyrin.application.services as application_services

from pyrin.core.structs import CoreObject
from pyrin.processor.cors.exceptions import CORSAllowedHeadersModificationError


class CORS(CoreObject):
    """
    cors class.
    """

    def __init__(self, **options):
        """
        initializes an instance of `CORS`.

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
        """

        super().__init__()

        self._enabled = options.get('cors_enabled')
        self._always_send = options.get('cors_always_send')
        self._allowed_origins = options.get('cors_allowed_origins')
        self._exposed_headers = options.get('cors_exposed_headers')
        self._allowed_headers = options.get('cors_allowed_headers')
        self._allow_credentials = options.get('cors_allow_credentials')
        self._max_age = options.get('cors_max_age')

    def add_allowed_headers(self, *headers):
        """
        adds given headers into allowed headers.

        :param str headers: headers to be added.

        :raises CORSAllowedHeadersModificationError: cors allowed headers modification error.
        """

        if application_services.got_first_request() is True:
            raise CORSAllowedHeadersModificationError('Cors allowed headers could not be '
                                                      'modified after first request is served.')

        if headers is not None and len(headers) > 0:
            current_headers = self._allowed_headers or []
            current_headers = set(current_headers).union(set(headers))
            self._allowed_headers = list(current_headers)

    @property
    def enabled(self):
        """
        gets a value indicating that cross origin resource sharing is enabled.

        :rtype: bool
        """

        return self._enabled

    @property
    def always_send(self):
        """
        gets a value indicating that cors headers must be included in response.

        even if the request does not have origin header.

        :rtype: bool
        """

        return self._always_send

    @property
    def allowed_origins(self):
        """
        gets a list of extra allowed origins to be used in conjunction with default allowed ones.

        :rtype: list[str]
        """

        return self._allowed_origins

    @property
    def allowed_headers(self):
        """
        gets a list of extra allowed headers to be used in conjunction with default allowed ones.

        :rtype: list[str]
        """

        return self._allowed_headers

    @property
    def exposed_headers(self):
        """
        gets a list of extra exposed headers to be used in conjunction with default exposed ones.

        :rtype: list[str]
        """

        return self._exposed_headers

    @property
    def allow_credentials(self):
        """
        gets a value indicating that browsers are allowed to pass response headers.

        to front-end javascript code.

        :rtype: bool
        """

        return self._allow_credentials

    @property
    def max_age(self):
        """
        gets the maximum number of seconds to cache results.

        :rtype: int
        """

        return self._max_age

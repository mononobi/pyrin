# -*- coding: utf-8 -*-
"""
cors services module.
"""

from pyrin.processor.cors import CORSPackage
from pyrin.application.services import get_component


def get_cors_headers(**options):
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

    return get_component(CORSPackage.COMPONENT_NAME).get_cors_headers(**options)


def get_preflight_headers(*allowed_methods, **options):
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

    return get_component(CORSPackage.COMPONENT_NAME).get_preflight_headers(*allowed_methods,
                                                                           **options)


def process_inputs(cors, **options):
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

    return get_component(CORSPackage.COMPONENT_NAME).process_inputs(cors, **options)


def get_required_cors_headers():
    """
    gets cors headers for current request if required.

    if cors conditions are not met, it returns None.

    :rtype: CoreHeaders
    """

    return get_component(CORSPackage.COMPONENT_NAME).get_required_cors_headers()


def get_required_preflight_headers():
    """
    gets preflight headers for current request if required.

    if any errors occurs or cors conditions are not met, it returns None.

    :rtype: CoreHeaders
    """

    return get_component(CORSPackage.COMPONENT_NAME).get_required_preflight_headers()


def get_current_cors_headers():
    """
    gets all required cors or preflight headers.

    it may return None if cors conditions are not met.

    :rtype: CoreHeaders
    """

    return get_component(CORSPackage.COMPONENT_NAME).get_current_cors_headers()

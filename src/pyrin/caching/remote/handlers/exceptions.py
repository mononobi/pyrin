# -*- coding: utf-8 -*-
"""
caching remote handlers exceptions module.
"""

from pyrin.core.exceptions import CoreException


class CachingRemoteHandlersException(CoreException):
    """
    caching remote handlers exception.
    """
    pass


class BothHostnameAndUnixSocketProvidedError(CachingRemoteHandlersException):
    """
    both hostname and unix socket provided error.
    """
    pass


class HostnameOrUnixSocketRequiredError(CachingRemoteHandlersException):
    """
    hostname or unix socket required error.
    """
    pass

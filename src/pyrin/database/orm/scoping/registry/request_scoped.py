# -*- coding: utf-8 -*-
"""
orm scoping request_scoped module.
"""

import pyrin.security.session.services as session_services

from pyrin.database.orm.scoping.registry.base import ScopedRegistryBase


class RequestScopedRegistry(ScopedRegistryBase):
    """
    request scoped registry class.

    this class provides a way to overcome the out of request
    context error when configuring sessions on application startup.
    """

    def safe_has(self):
        """
        gets a value indicating that an object is present in the current scope.

        note that the difference between this method and `has()` method is that
        if the `scopefunc()` which is bounded to request is not ready to be used
        and raises an error, this function returns False instead of raising that
        error. this method is needed for when the application wants to configure
        sessions on startup and the `scopefunc` is not usable at that moment yet,
        because there is no request object available.
        """

        if session_services.is_request_context_available() is True:
            return super().has()

        return False

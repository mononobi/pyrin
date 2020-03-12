# -*- coding: utf-8 -*-
"""
orm scoping thread_scoped module.
"""

from sqlalchemy.util import ThreadLocalRegistry

from pyrin.database.orm.scoping.registry.request_scoped import RequestScopedRegistry


class ThreadScopedRegistry(ThreadLocalRegistry, RequestScopedRegistry):
    """
    thread scoped registry class.
    """

    def safe_has(self):
        """
        gets a value indicating that an object is present in the current scope.

        note that the difference between this method and `has()` method is that
        if the `scopefunc()` is not ready to be used and raises an error, this
        function should return False instead of raising that error.
        """

        return super().has()

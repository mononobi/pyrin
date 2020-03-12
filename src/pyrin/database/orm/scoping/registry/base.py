# -*- coding: utf-8 -*-
"""
orm scoping registry base module.
"""

from abc import abstractmethod

from sqlalchemy.util import ScopedRegistry

from pyrin.core.exceptions import CoreNotImplementedError


class ScopedRegistryBase(ScopedRegistry):
    """
    scoped registry base class.

    all application scoped registry classes must be subclassed from this.
    """

    @abstractmethod
    def safe_has(self):
        """
        gets a value indicating that an object is present in the current scope.

        note that the difference between this method and `has()` method is that
        if the `scopefunc()` is not ready to be used and raises an error, this
        function should return False instead of raising that error.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

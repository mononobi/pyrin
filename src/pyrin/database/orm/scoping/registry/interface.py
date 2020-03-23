# -*- coding: utf-8 -*-
"""
orm scoping registry interface module.
"""

from abc import abstractmethod

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.core.structs import CoreObject


class AbstractAtomicContainerBase(CoreObject):
    """
    abstract atomic container base class.
    """

    @abstractmethod
    def has(self):
        """
        gets a value indicating that an atomic object is present in the current scope.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def set(self, obj):
        """
        sets an atomic value for the current scope.

        :param object obj: object to be set in registry.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def clear(self, atomic=False):
        """
        clears all objects of current scope, if any.

        if `atomic=True` is provided, it only clears the
        current atomic object if available.

        :param bool atomic: specifies that it must only clear the current atomic
                            object of current scope. otherwise, it clears all atomic
                            objects of current scope. defaults to False if not provided.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get(self):
        """
        gets the current atomic object of current scope if available, otherwise returns None.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: object
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get_all(self):
        """
        gets all atomic objects of current scope if available, otherwise returns an empty list.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: list[object]
        """

        raise CoreNotImplementedError()

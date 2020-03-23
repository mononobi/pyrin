# -*- coding: utf-8 -*-
"""
orm scoping interface module.
"""

from abc import abstractmethod

from pyrin.core.structs import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError


class AbstractScopedRegistryBase(CoreObject):
    """
    abstract scoped registry base class.

    all application scoped registry classes must be subclassed from this.
    it also supports atomic objects.
    """

    @abstractmethod
    def __call__(self, atomic=False):
        """
        gets the corresponding object from registry if available, otherwise creates a new one.

        note that if there is an atomic object available, and `atomic=False` is
        provided, it always returns the available atomic object, but if `atomic=True`
        is provided it always creates a new atomic object.

        :param bool atomic: specifies that it must get a new atomic object.
                            defaults to False if not provided.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: object
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def has(self, atomic=False):
        """
        gets a value indicating that an object is present in the current scope.

        :param bool atomic: specifies that it must check just for an atomic
                            object. defaults to False if not provided.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def set(self, obj, atomic=False):
        """
        sets the value for the current scope.

        :param object obj: object to be set in registry.

        :param bool atomic: specifies that it must set an atomic object.
                            defaults to False if not provided.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def clear(self, atomic=False):
        """
        clears the current scope's objects, if any.

        it also clears if any atomic object is available.
        if `atomic=True` is provided, it only clears the
        current atomic object if available.

        :param bool atomic: specifies that it must only clear the current atomic
                            object of current scope. otherwise, it clears all objects
                            of current scope. defaults to False if not provided.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def clear_all_atomic(self):
        """
        clears all atomic objects of current scope, if any.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get(self, atomic=False):
        """
        gets the current object of current scope if available, otherwise returns None.

        :param bool atomic: specifies that it must get the current atomic object of
                            current scope, otherwise it returns the normal object.
                            defaults to False if not provided.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: object
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get_all_atomic(self):
        """
        gets all atomic objects of current scope if available, otherwise returns an empty list.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: list[object]
        """

        raise CoreNotImplementedError()

    def inject_atomic(self, value, atomic=False):
        """
        injects the given atomic flag into given value and returns the same value.

        :param object value: value to inject atomic flag to it.

        :param bool atomic: indicates that the value should be marked
                            as atomic. defaults to False if not provided.

        :returns: object
        """

        setattr(value, 'atomic', atomic)
        return value

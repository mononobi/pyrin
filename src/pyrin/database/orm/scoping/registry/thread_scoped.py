# -*- coding: utf-8 -*-
"""
orm scoping registry thread_scoped module.
"""

from sqlalchemy.util import ThreadLocalRegistry

from pyrin.database.orm.scoping.interface import AbstractScopedRegistryBase


class ThreadScopedRegistry(ThreadLocalRegistry, AbstractScopedRegistryBase):
    """
    thread scoped registry class.

    it also supports atomic objects.
    """

    def __call__(self, atomic=False):
        """
        gets the corresponding object from registry if available, otherwise creates a new one.

        note that if there is an atomic object available,
        it always returns it, even if `atomic=False` is provided.

        :param bool atomic: specifies that it must get an atomic object.
                            it returns it from registry if available,
                            otherwise gets a new atomic object.
                            defaults to False if not provided.

       :returns: object
        """

        try:
            return self.registry.atomic_value
        except AttributeError:
            if atomic is True:
                atomic_value = self.registry.atomic_value = self.inject_atomic(
                    self.createfunc(), True)
                return atomic_value

        return super().__call__()

    def has(self, atomic=False):
        """
        gets a value indicating that an object is present in the current scope.

        :param bool atomic: specifies that it must check just for an atomic
                            object. defaults to False if not provided.

        :rtype: bool
        """

        has_atomic = hasattr(self.registry, "atomic_value")
        if atomic is True:
            return has_atomic
        return has_atomic or super().has()

    def set(self, obj, atomic=False):
        """
        sets the value for the current scope.

        :param object obj: object to be set in registry.

        :param bool atomic: specifies that it must set an atomic object.
                            defaults to False if not provided.
        """

        if atomic is True:
            self.registry.atomic_value = obj
        else:
            super().set(obj)

    def clear(self, atomic=False):
        """
        clears the current scope's object, if any.

        it also clears if any atomic object is available.
        if `atomic=True` is provided, it only clears the atomic object if available.

        :param bool atomic: specifies that it must only clear an atomic object
                            of current scope. otherwise, it clears all objects of
                            current scope. defaults to False if not provided.
        """

        try:
            del self.registry.atomic_value
        except AttributeError:
            pass

        if atomic is False:
            return super().clear()

    def get(self, atomic=False):
        """
        gets the current object of this scope if available, otherwise returns None.

        :param bool atomic: specifies that it must get the atomic object of
                            current scope, otherwise it returns the normal object.
                            defaults to False if not provided.

        :rtype: object
        """

        if atomic is True:
            return self._get_atomic()

        return self._get()

    def _get_atomic(self):
        """
        gets the current atomic object of this scope if available, otherwise returns None.

        :rtype: object
        """

        try:
            return self.registry.atomic_value
        except AttributeError:
            return None

    def _get(self):
        """
        gets the current normal object of this scope if available, otherwise returns None.

        :rtype: object
        """

        try:
            return self.registry.value
        except AttributeError:
            return None

# -*- coding: utf-8 -*-
"""
orm scoping registry thread_scoped module.
"""

from sqlalchemy.util import ThreadLocalRegistry

from pyrin.database.orm.scoping.interface import AbstractScopedRegistryBase
from pyrin.database.orm.scoping.registry.containers.atomic import ThreadScopedAtomicContainer


class ThreadScopedRegistry(ThreadLocalRegistry, AbstractScopedRegistryBase):
    """
    thread scoped registry class.

    it also supports atomic objects.
    """

    def __init__(self, createfunc):
        """
        initializes and instance of ThreadScopedRegistry.

        :param function createfunc: a creation function that will generate a new
                                    value for the current scope, if none is present.
        """

        super().__init__(createfunc)

        self.atomic_registry = ThreadScopedAtomicContainer()

    def __call__(self, atomic=False):
        """
        gets the corresponding object from registry if available, otherwise creates a new one.

        note that if there is an atomic object available, and `atomic=False` is
        provided, it always returns the available atomic object, but if `atomic=True`
        is provided it always creates a new atomic object.

        :param bool atomic: specifies that it must get a new atomic object.
                            defaults to False if not provided.

       :returns: object
        """

        if atomic is True:
            value = self.inject_atomic(self.createfunc(), atomic)
            self.set(value, atomic)
            return value

        value = self.atomic_registry.get()
        if value is not None:
            return value

        return self.inject_atomic(super().__call__(), atomic)

    def has(self, atomic=False):
        """
        gets a value indicating that an object is present in the current scope.

        :param bool atomic: specifies that it must check just for an atomic
                            object. defaults to False if not provided.

        :rtype: bool
        """

        has_atomic = self.atomic_registry.has()
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
            self.atomic_registry.set(obj)
        else:
            super().set(obj)

    def clear(self, atomic=False):
        """
        clears the current scope's object, if any.

        it also clears if any atomic object is available.
        if `atomic=True` is provided, it only clears the
        current atomic object if available.

        :param bool atomic: specifies that it must only clear the current atomic
                            object of current scope. otherwise, it clears all objects
                            of current scope. defaults to False if not provided.
        """

        self.atomic_registry.clear(atomic)
        if atomic is False:
            return super().clear()

    def clear_all_atomic(self):
        """
        clears all atomic objects of current scope, if any.
        """

        self.atomic_registry.clear()

    def get(self, atomic=False):
        """
        gets the current object of current scope if available, otherwise returns None.

        :param bool atomic: specifies that it must get the atomic object of
                            current scope, otherwise it returns the normal object.
                            defaults to False if not provided.

        :rtype: object
        """

        if atomic is True:
            return self._get_atomic()

        return self._get()

    def get_all_atomic(self):
        """
        gets all atomic objects of current scope if available, otherwise returns an empty list.

        :rtype: list[object]
        """

        return self.atomic_registry.get_all()

    def _get_atomic(self):
        """
        gets the current atomic object of current scope if available, otherwise returns None.

        :rtype: object
        """

        return self.atomic_registry.get()

    def _get(self):
        """
        gets the current normal object of current scope if available, otherwise returns None.

        :rtype: object
        """

        try:
            return self.registry.value
        except AttributeError:
            return None

# -*- coding: utf-8 -*-
"""
orm scoping registry request_scoped module.
"""

from sqlalchemy.util import ScopedRegistry

import pyrin.security.session.services as session_services

from pyrin.database.orm.scoping.interface import AbstractScopedRegistryBase


class RequestScopedRegistry(ScopedRegistry, AbstractScopedRegistryBase):
    """
    request scoped registry class.

    this class provides a way to overcome the out of request
    context error when configuring sessions on application startup.
    it also supports atomic objects.
    """

    def __init__(self, createfunc, scopefunc):
        """
        initializes and instance of RequestScopedRegistry.

        :param callable createfunc: a creation function that will generate a new
                                    value for the current scope, if none is present.

        :param callable scopefunc: a function that returns a hashable
                                   token representing the current scope.
                                   such as, current thread identifier.
        """

        super().__init__(createfunc, scopefunc)

        # a dictionary containing all atomic sessions that are present.
        # each atomic session corresponds to a request scoped session.
        # in the form of: {hash key: CoreSession session}
        self.atomic_registry = {}

    def __call__(self, atomic=False):
        """
        gets the corresponding object from registry if available, otherwise creates a new one.

        note that if there is an atomic object available,
        it always returns it, even if `atomic=False` is provided.

        :param bool atomic: specifies that it must get an atomic object.
                            it returns it from atomic registry if available,
                            otherwise gets a new atomic object.
                            defaults to False if not provided.

        :returns: object
        """

        key = self.scopefunc()
        try:
            return self.atomic_registry[key]
        except KeyError:
            if atomic is True:
                return self.atomic_registry.setdefault(key, self.inject_atomic(
                    self.createfunc(), True))

        return super().__call__()

    def has(self, atomic=False):
        """
        gets a value indicating that an object is present in the current scope.

        :param bool atomic: specifies that it must check just for an atomic
                            object. defaults to False if not provided.

        :rtype: bool
        """

        if session_services.is_request_context_available() is True:
            has_atomic = self.scopefunc() in self.atomic_registry
            if atomic is True:
                return has_atomic
            return has_atomic or super().has()

        return False

    def set(self, obj, atomic=False):
        """
        sets the value for the current scope.

        :param object obj: object to be set in registry.

        :param bool atomic: specifies that it must set an atomic object.
                            defaults to False if not provided.
        """

        if atomic is True:
            self.atomic_registry[self.scopefunc()] = obj
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
            del self.atomic_registry[self.scopefunc()]
        except KeyError:
            pass

        if atomic is False:
            super().clear()

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
            return self.atomic_registry[self.scopefunc()]
        except KeyError:
            return None

    def _get(self):
        """
        gets the current normal object of this scope if available, otherwise returns None.

        :rtype: object
        """

        try:
            return self.registry[self.scopefunc()]
        except KeyError:
            return None

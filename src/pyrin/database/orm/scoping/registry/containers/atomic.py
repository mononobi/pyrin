# -*- coding: utf-8 -*-
"""
orm scoping registry containers atomic module.
"""

import threading

import pyrin.security.session.services as session_services

from pyrin.core.structs import Stack
from pyrin.database.orm.scoping.registry.interface import AbstractAtomicContainerBase


class RequestScopedAtomicContainer(AbstractAtomicContainerBase):
    """
    request scoped atomic container class.
    """

    def __init__(self, scopefunc):
        """
        initializes an instance of RequestScopedAtomicContainer.

        :param function scopefunc: a function that returns a hashable
                                   token representing the current scope.
                                   such as, current thread identifier.
        """

        super().__init__()

        self.scopefunc = scopefunc

        # a dictionary containing all atomic sessions that are present.
        # each atomic session corresponds to a request scoped session.
        # each request could contain a 'Stack' of current atomic sessions.
        # each time an atomic session is requested, it gets the last inserted
        # atomic session, this way it provides the ability to use chained
        # atomic sessions. for example multiple methods using '@atomic' decorator
        # in a single call hierarchy.
        # in the form of: {int key_hash: Stack[object] objects}
        self.registry = {}

    def has(self):
        """
        gets a value indicating that an atomic object is present in the current scope.

        :rtype: bool
        """

        if session_services.is_request_context_available() is True:
            return self.scopefunc() in self.registry

        return False

    def set(self, value):
        """
        sets an atomic value for the current scope.

        :param object value: object to be set in registry.
        """

        stack = self._get_stack(True)
        stack.push(value)

    def clear(self, atomic=False):
        """
        clears the current scope's atomic objects, if any.

        if `atomic=True` is provided, it only clears the
        current atomic object if available.

        :param bool atomic: specifies that it must only clear the current atomic
                            object of current scope. otherwise, it clears all atomic
                            objects of current scope. defaults to False if not provided.
        """

        if atomic is True:
            try:
                self._get_stack().dispose()
            except (KeyError, IndexError):
                pass

            if self._get_stack_length() == 0:
                self._clear_all()
        else:
            self._clear_all()

    def _clear_all(self):
        """
        clears all atomic objects of current scope, if any.
        """

        try:
            del self.registry[self.scopefunc()]
        except KeyError:
            pass

    def get(self):
        """
        gets the current atomic object of current scope if available, otherwise returns None.

        :returns: object
        """

        try:
            return self._get_stack().peek()
        except (KeyError, IndexError):
            return None

    def get_all(self):
        """
        gets all atomic objects of current scope if available, otherwise returns an empty list.

        :returns: list[object]
        """

        try:
            return self._get_stack().peek_all()
        except KeyError:
            return []

    def _get_stack(self, create=False):
        """
        gets the stack of current scope if available.

        otherwise it could either return a new stack or raise an error.

        :param bool create: specifies that if there is no stack available,
                            it should return a new stack, otherwise raise
                            an error. defaults to False if not provided.

        :raises KeyError: key error.

        :rtype: Stack
        """

        key = self.scopefunc()
        try:
            return self.registry[key]
        except KeyError as error:
            if create is True:
                return self.registry.setdefault(key, Stack())
            raise error

    def _get_stack_length(self):
        """
        gets the length of items in the stack of current scope if available.

        if there is no stack available, it returns -1.

        :rtype: int
        """

        try:
            return len(self._get_stack())
        except KeyError:
            return -1


class ThreadScopedAtomicContainer(AbstractAtomicContainerBase):
    """
    thread scoped atomic container class.
    """

    def __init__(self):
        """
        initializes an instance of ThreadScopedAtomicContainer.
        """

        super().__init__()

        self.registry = threading.local()

    def has(self):
        """
        gets a value indicating that an atomic object is present in the current scope.

        :rtype: bool
        """

        return hasattr(self.registry, "stack")

    def set(self, value):
        """
        sets an atomic value for the current scope.

        :param object value: object to be set in registry.
        """

        stack = self._get_stack(True)
        stack.push(value)

    def clear(self, atomic=False):
        """
        clears the current scope's atomic objects, if any.

        if `atomic=True` is provided, it only clears the
        current atomic object if available.

        :param bool atomic: specifies that it must only clear the current atomic
                            object of current scope. otherwise, it clears all atomic
                            objects of current scope. defaults to False if not provided.
        """

        if atomic is True:
            try:
                self._get_stack().dispose()
            except (AttributeError, IndexError):
                pass

            if self._get_stack_length() == 0:
                self._clear_all()
        else:
            self._clear_all()

    def _clear_all(self):
        """
        clears all atomic objects of current scope, if any.
        """

        try:
            del self.registry.stack
        except AttributeError:
            pass

    def get(self):
        """
        gets the current atomic object of current scope if available, otherwise returns None.

        :returns: object
        """

        try:
            return self._get_stack().peek()
        except (AttributeError, IndexError):
            return None

    def get_all(self):
        """
        gets all atomic objects of current scope if available, otherwise returns an empty list.

        :returns: list[object]
        """

        try:
            return self._get_stack().peek_all()
        except AttributeError:
            return []

    def _get_stack(self, create=False):
        """
        gets the stack of current scope if available.

        otherwise it could either return a new stack or raise an error.

        :param bool create: specifies that if there is no stack available,
                            it should return a new stack, otherwise raise
                            an error. defaults to False if not provided.

        :raises AttributeError: attribute error.

        :rtype: Stack
        """

        try:
            return self.registry.stack
        except AttributeError as error:
            if create is True:
                self.registry.stack = Stack()
                return self.registry.stack
            raise error

    def _get_stack_length(self):
        """
        gets the length of items in the stack of current scope if available.

        if there is no stack available, it returns -1.

        :rtype: int
        """

        try:
            return len(self._get_stack())
        except AttributeError:
            return -1

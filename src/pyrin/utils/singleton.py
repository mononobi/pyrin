# -*- coding: utf-8 -*-
"""
utils singleton module.
"""

from threading import Lock

from pyrin.core.exceptions import CoreNotImplementedError


class SingletonMetaBase(type):
    """
    singleton meta base class.
    this is a thread-safe implementation of singleton.
    """

    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        try:
            cls._lock.acquire()
            if cls._has_instance() is False:
                instance = super().__call__(*args, **kwargs)
                cls._register_instance(instance)
        finally:
            if cls._lock.locked():
                cls._lock.release()

        return cls._get_instance()

    def _has_instance(cls):
        """
        gets a value indicating there is a registered instance.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    def _register_instance(cls, instance):
        """
        registers the given instance.

        :param object instance: instance to be registered.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    def _get_instance(cls):
        """
        gets the registered instance.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: object
        """

        raise CoreNotImplementedError()


class UniqueSingletonMeta(SingletonMetaBase):
    """
    unique singleton meta class.
    this is a thread-safe implementation of singleton.
    this class only allows a single unique object for all descendant types.

    for example: {Base -> UniqueSingletonMeta, A -> Base, B -> A}
    if some_object = Base() then always Base() = A() = B() = some_object.
    or if some_object = A() then always A() = B() = some_object != Base().
    """

    _instance = None
    _lock = Lock()

    def _has_instance(cls):
        """
        gets a value indicating that there is a registered instance.

        :rtype: bool
        """

        return cls._instance is not None

    def _register_instance(cls, instance):
        """
        registers the given instance.
        """

        cls._instance = instance

    def _get_instance(cls):
        """
        gets the registered instance.

        :rtype: object
        """

        return cls._instance


class MultiSingletonMeta(SingletonMetaBase):
    """
    multi singleton meta class.
    this is a thread-safe implementation of singleton.
    this class allows a unique object per each type of descendants.

    for example: {Base -> UniqueSingletonMeta, A -> Base, B -> A}
    if some_object = Base() then always Base() != A() != B() but always Base() = some_object.
    or if some_object = A() then always Base() != A() != B() but always A() = some_object.
    """

    # a dictionary containing an instance of each type.
    # in the form of: {type: instance}
    _instances = dict()
    _lock = Lock()

    def _has_instance(cls):
        """
        gets a value indicating that there is a registered instance.

        :rtype: bool
        """

        return str(cls) in cls._instances

    def _register_instance(cls, instance):
        """
        registers the given instance.
        """

        cls._instances[str(cls)] = instance

    def _get_instance(cls):
        """
        gets the registered instance.

        :rtype: object
        """

        return cls._instances.get(str(cls))

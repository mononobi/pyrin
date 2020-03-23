# -*- coding: utf-8 -*-
"""
core structs module.
"""

from collections import deque
from threading import Lock
from abc import abstractmethod

from pyrin.core.exceptions import CoreAttributeError, ContextAttributeError, \
    CoreNotImplementedError


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

    @abstractmethod
    def _has_instance(cls):
        """
        gets a value indicating there is a registered instance.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _register_instance(cls, instance):
        """
        registers the given instance.

        :param object instance: instance to be registered.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
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


class DTO(dict):
    """
    context class for storing objects in every layer.

    it's actually a dictionary with the capability to treat keys as instance attributes.
    this class's objects are hashable and could be used as a dict key if needed.
    """

    def __getattr__(self, name):
        if name in self:
            return self.get(name)

        raise CoreAttributeError('Property [{name}] not found.'.format(name=name))

    def __getitem__(self, item):
        if item in self:
            return self.get(item)

        raise CoreAttributeError('Property [{name}] not found.'.format(name=item))

    def __setattr__(self, name, value):
        self[name] = value

    def __hash__(self):
        signature = None
        try:
            # try to sort by keys if all keys are same type.
            signature = sorted(self.items())
        except TypeError:
            # fallback to unsorted keys when key types are incomparable.
            signature = self.items()
        return hash(tuple(signature))

    def __eq__(self, other):
        if not isinstance(other, DTO):
            return False

        self_len = len(self)
        other_len = len(other)
        if self_len != other_len:
            return False

        if self_len == 0:
            return True

        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self == other


class CoreObject(object):
    """
    core object class.

    this should be used as the base object for all application objects.
    """

    def __init__(self):
        """
        initializes an instance of CoreObject.
        """

        super().__init__()
        self.__name = None

    def __setattr__(self, name, value):
        return self._setattr(name, value)

    def __repr__(self):
        """
        gets the string representation of current object.

        :rtype: str
        """

        return str(self)

    def __str__(self):
        """
        gets the string representation of current object.

        :rtype: str
        """

        return '{module}.{name}'.format(module=self.__module__,
                                        name=self.__class__.__name__)

    def get_name(self):
        """
        gets the name of the object.

        if name is not available, returns its class name.

        :rtype: str
        """

        if self.__name is not None:
            return self.__name
        return self.get_class_name()

    def _set_name(self, name):
        """
        sets new name to current object.

        :param str name: object new name.
        """

        self.__name = name

    def get_class_name(self):
        """
        gets the object's class name.

        :rtype: str
        """

        return self.__class__.__name__

    def get_module_name(self):
        """
        gets the object's module name.

        :rtype: str
        """

        return self.__class__.__module__

    def get_doc(self):
        """
        gets the docstring of the object.

        :rtype: str
        """

        return self.__doc__

    def _setattr(self, name, value):
        """
        sets the given value to specified attribute.

        :param str name: attribute name.
        :param object value: attribute value.
        """

        return super().__setattr__(name, value)


class Context(DTO):
    """
    context class for storing objects in every layer.

    it's actually a dictionary with the capability to add keys directly.
    """

    def __getattr__(self, name):
        if name in self:
            return self.get(name)

        self._raise_key_error(name)

    def __getitem__(self, item):
        if item in self:
            return self.get(item)

        self._raise_key_error(item)

    def _raise_key_error(self, key):
        """
        raises an error for given key.

        :param object key: key object that caused the error.

        :raises ContextAttributeError: context attribute error.
        """

        raise ContextAttributeError('Property [{name}] not found.'.format(name=key))


class HookSingletonMeta(MultiSingletonMeta):
    """
    hook singleton meta class.

    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class Hook(CoreObject, metaclass=HookSingletonMeta):
    """
    base hook class.

    all application hook classes must be subclassed from this one.
    """
    pass


class ManagerSingletonMeta(MultiSingletonMeta):
    """
    manager singleton meta class.

    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class Manager(CoreObject, metaclass=ManagerSingletonMeta):
    """
    base manager class.

    all application manager classes must be subclassed from this one.
    """
    pass


class CLISingletonMeta(MultiSingletonMeta):
    """
    cli singleton meta class.

    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class CLI(CoreObject, metaclass=CLISingletonMeta):
    """
    base cli class.

    all application cli classes must be subclassed from this one.
    """

    # this value must be set in each subclass with the relevant callable
    # execute service with the param signature of: `(str handler_name, **inputs)`
    _execute_service = None

    @classmethod
    def execute(cls, handler_name, **options):
        """
        executes the handler with the given name with given inputs.

        :param str handler_name: handler name to be executed.

        :raises CLIHandlerNotFoundError: cli handler not found error.

        :rtype: int
        """

        return cls._execute_service(handler_name, **options)


class Stack(deque):
    """
    stack class.

    this class extends `deque` and provides a `peek()` method to
    just get the top most item without removing it.
    it also provides some other useful methods for convenient of usage.

    note that `Stack` is not guaranteed to be thread-safe on all python
    implementations, because it extends `deque`. so do not use it when
    there is a multi-thread access to the same stack.
    """

    def peek(self):
        """
        gets the top most item of stack, without removing it.

        the return value of `peek()` is the same as `pop()`
        but without removing it from the stack.
        if the stack is empty, it raises an error.

        :raises IndexError: index error.

        :rtype: object
        """

        return self[-1]

    def peek_all(self):
        """
        gets all items of stack, without removing them.

        the result is a list of all items of the stack in the order of
        `peek()`. meaning that, last inserted items will be in lower indices.

        :rtype: list[object]
        """

        return list(reversed(self))

    def push(self, value):
        """
        adds the given value into top of stack.

        :param object value: value to be added into stack.

        this method is just implemented for convenient of usage,
        it will call `append()` under the hood.
        """

        self.append(value)

    def dispose(self):
        """
        deletes the top most item of stack, without returning it.

        if the stack is empty, it raises an error.

        :raises IndexError: index error.
        """

        del self[-1]

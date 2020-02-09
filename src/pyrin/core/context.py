# -*- coding: utf-8 -*-
"""
core context module.
"""

from threading import Lock

from pyrin.core.exceptions import CoreAttributeError, ContextAttributeError
from pyrin.utils.singleton import MultiSingletonMeta


class DTO(dict):
    """
    context class for storing objects in every layer.
    it's actually a dictionary with the capability to treat keys as instance attributes.
    this class's objects are immutable and could be used as a dict key if needed.
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
    base object for all application objects.
    """

    def __init__(self):
        super().__init__()
        self.__name = None

    def get_name(self):
        """
        gets the name of the object.
        if name is not available, returns its class name.

        :rtype: str
        """

        if self.__name is not None:
            return self.__name
        return self.__class__.__name__

    def _set_name(self, name):
        """
        sets new name to current object.

        :param str name: object new name.
        """

        self.__name = name

    def get_doc(self):
        """
        gets docstring of the object.

        :rtype: str
        """

        return self.__doc__

    def setattr(self, name, value):
        """
        sets the given value to specified attribute.

        :param str name: attribute name.
        :param object value: attribute value.
        """

        return super().__setattr__(name, value)

    def __setattr__(self, name, value):
        return self.setattr(name, value)


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
    pass

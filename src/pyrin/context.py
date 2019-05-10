# -*- coding: utf-8 -*-
"""
pyrin context module.
"""

from enum import Enum, EnumMeta

from pyrin.exceptions import CoreAttributeError


class DTO(dict):
    """
    context class for storing objects in every layer.
    it's actually a dictionary with the capability to add keys directly.
    """

    def __getattr__(self, name):
        if name in self:
            return self.get(name)

        raise CoreAttributeError('Property [{name}] not found.'.format(name=name))

    def __setattr__(self, name, value):
        self[name] = value

    def __hash__(self):
        return hash(tuple(self.values()))

    def __eq__(self, other):
        if not other or not isinstance(other, DTO):
            return False
        keys = self.keys()
        if len(keys) != len(other.keys()):
            return False
        for key in keys:
            if self.get(key, None) != other.get(key, None):
                return False
        return True


class CoreObject(object):
    """
    base class for all application classes.
    """

    def __init__(self):
        object.__init__(self)
        self.__name = None

    def get_name(self):
        """
        gets the name of the object.
        if name is not available, returns objects's class name.

        :rtype: str
        """

        if self.__name:
            return self.__name
        return self.__class__.__name__

    def _set_name_(self, name):
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

        return object.__setattr__(self, name, value)

    def __setattr__(self, name, value):
        return self.setattr(name, value)


class ContextAttributeError(CoreAttributeError):
    """
    context attribute error.
    """
    pass


class Context(DTO):
    """
    context class for storing objects in every layer.
    it's actually a dictionary with the capability to add keys directly.
    """

    def __getattr__(self, name):
        if name in self:
            return self.get(name)

        raise ContextAttributeError('Property [{name}] not found.'.format(name=name))


class Component(CoreObject):
    """
    base component class.
    all component classes must inherit from this class and their respective manager class.
    """

    # COMPONENT_ID should be unique for each instance.
    COMPONENT_ID = ''

    def __init__(self, **options):
        """
        initializes an instance of Component.
        """

        super(Component, self).__init__()


class CoreEnumMeta(EnumMeta):
    """
    base enum metaclass.
    """
    pass


class CoreEnum(Enum, metaclass=CoreEnumMeta):
    """
    base enum class.
    all application enumerations must inherit from this class.
    """

    def __get__(self, instance, owner):
        return self.value

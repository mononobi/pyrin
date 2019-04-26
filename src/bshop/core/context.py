# -*- coding: utf-8 -*-
"""
Core context module.
"""

from enum import Enum, EnumMeta

from bshop.core.exceptions import CoreAttributeError


class DynamicObject(dict):
    """
    Context class for storing objects in every layer.
    It's actually a dictionary with the capability to add keys directly.
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
        if not other or not isinstance(other, DynamicObject):
            return False
        keys = self.keys()
        if len(keys) != len(other.keys()):
            return False
        for key in keys:
            if self.get(key, None) != other.get(key, None):
                return False
        return True


class ObjectBase(object):
    """
    Base class for all application classes.
    """

    def __init__(self):
        object.__init__(self)
        self.__name = None

    def get_name(self):
        """
        Gets the name of the object.

        :rtype: str
        """

        if self.__name:
            return self.__name
        return self.__class__.__name__

    def _set_name_(self, name):
        """
        Sets new name to current object.

        :param str name: object new name.
        """

        self.__name = name

    def get_doc(self):
        """
        Gets docstring of the object.

        :rtype: str
        """

        return self.__doc__

    def setattr(self, name, value):
        """
        Sets the given value to specified attribute.

        :param str name: attribute name.
        :param object value: attribute value.
        """

        return object.__setattr__(self, name, value)

    def __setattr__(self, name, value):
        return self.setattr(name, value)


class ContextAttributeError(CoreAttributeError):
    """
    Context attribute error.
    """
    pass


class Context(DynamicObject):
    """
    Context class for storing objects in every layer.
    It's actually a dictionary with the capability to add keys directly.
    """

    def __getattr__(self, name):
        if name in self:
            return self.get(name)

        raise ContextAttributeError('Property [{name}] not found.'.format(name=name))


class Component(ObjectBase):
    """
    Base component class.
    All manager classes must inherit from this class.
    """

    # COMPONENT_ID should be unique for each instance.
    COMPONENT_ID = ''


class EnumMetaBase(EnumMeta):
    """
    Base enum metaclass.
    """
    pass


class EnumBase(Enum, metaclass=EnumMetaBase):
    """
    Base enum class.
    All application enumerations must inherit from this class.
    """
    pass

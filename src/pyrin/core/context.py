# -*- coding: utf-8 -*-
"""
core context module.
"""

from enum import Enum, EnumMeta

from pyrin.core.exceptions import CoreAttributeError, ContextAttributeError
from pyrin.settings.static import DEFAULT_COMPONENT_KEY


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

        return object.__setattr__(self, name, value)

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

        raise ContextAttributeError('Property [{name}] not found.'.format(name=name))


class Component(CoreObject):
    """
    base component class.
    all component classes must inherit from this class and their respective manager class.
    """

    def __init__(self, component_name, **options):
        """
        initializes an instance of Component.

        :param str component_name: component name.

        :keyword object component_custom_key: component custom key.
        """

        super(Component, self).__init__()

        # component id is a tuple(str, object) and should be unique for each
        # instance unless it's intended to replace an already existing one.
        self._component_id = (component_name,
                              options.get('component_custom_key', DEFAULT_COMPONENT_KEY))

    def get_id(self):
        """
        gets the component id of this instance.

        :rtype: tuple(str, object)
        """

        return self._component_id


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
        """
        this method is overridden to be able to access enum
        member value without having to write `enum_member.value`.
        this causes `enum_member.name` to become unavailable.
        """

        return self.value

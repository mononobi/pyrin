# -*- coding: utf-8 -*-
"""
Defines base classes.
"""


class DynamicObject(dict):
    """
    Context class for storing objects in every layer.
    It's actually a dictionary with the capability to add keys directly.
    """

    def __getattr__(self, name):
        if name in self:
            return self.get(name)

        raise AttributeError('Property [{name}] not found.'.format(name=name))

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


class ExceptionBase(Exception):
    """
    Base class for all application exceptions.
    """

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

        self._data = {}
        self._traceback = None

    def get_code(self):
        """
        Gets the error code.

        :rtype: str
        """

        return self.__class__.__name__

    def get_data(self):
        """
        Gets the error data.

        :rtype: dict
        """

        return self._data

    def get_traceback(self):
        """
        Returns the traceback of this exception.

        :rtype: object
        """

        return self._traceback


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

        :param str name: object new name
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

        :param str name: attribute name
        :param object value: attribute value
        """

        return object.__setattr__(self, name, value)

    def __setattr__(self, name, value):

        return self.setattr(name, value)

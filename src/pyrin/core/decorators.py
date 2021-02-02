# -*- coding: utf-8 -*-
"""
core decorators module.
"""


class class_property(object):
    """
    a decorator to define a class property.

    it is similar to a property but works at class level.
    it only supports get.

    usage example:

    @class_property
    def name(cls):
        return cls.VALUE
    """

    def __init__(self, method=None):
        """
        initializes an instance of class_property.

        :param function method: decorated method.
        """

        self.fget = method

    def __get__(self, instance, cls=None):
        """
        gets the result of decorated method.

        :param instance: instance of parent class.
        :param type cls: class type.

        :returns: decorated method result.
        """

        if cls is None:
            cls = type(instance)

        return self.fget(cls)

    def getter(self, method):
        """
        returns current instance with its getter set to given method.

        :param function method: decorated method.

        :rtype: class_property
        """

        self.fget = method
        return self

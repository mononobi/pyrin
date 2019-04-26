# -*- coding: utf-8 -*-
"""
Deserializers decorators module.
"""

from bshop.core.api.deserializers import _register_deserializer
from bshop.core.api.deserializers.base import DeserializerBase
from bshop.core.exceptions import CoreTypeError


def register(*args, **kwargs):
    """
    Decorator to register a deserializer.

    :param object args: deserializer class constructor arguments.
    :param dict kwargs: deserializer class constructor keyword arguments.

    :returns: deserializer class.

    :rtype: type
    """

    def decorator(cls):
        """
        Decorates the given class and registers an instance
        of it into available deserializers.

        :param type cls: deserializer class.

        :raises CoreTypeError: core type error.

        :returns: deserializer class.

        :rtype: type
        """

        if not issubclass(cls, DeserializerBase):
            raise CoreTypeError('Input parameter [{class_name}] is '
                                'not a subclass of DeserializerBase.'
                                .format(class_name=str(cls)))

        instance = cls(*args, **kwargs)
        _register_deserializer(instance)

        return cls

    return decorator

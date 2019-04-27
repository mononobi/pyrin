# -*- coding: utf-8 -*-
"""
Deserializers decorators module.
"""

import bshop.core.api.deserializers.services as deserializer_services

from bshop.core.api.deserializers.handlers.base import DeserializerBase
from bshop.core.exceptions import CoreTypeError


def register(*args, **kwargs):
    """
    Decorator to register a deserializer.

    :param object args: deserializer class constructor arguments.
    :param object kwargs: deserializer class constructor keyword arguments.

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
        deserializer_services.register_deserializer(instance, **kwargs)

        return cls

    return decorator

# -*- coding: utf-8 -*-
"""
deserializer decorators module.
"""

import pyrin.converters.deserializer.services as deserializer_services

from pyrin.converters.deserializer.handlers.base import DeserializerBase
from pyrin.exceptions import CoreTypeError


def deserializer(*args, **kwargs):
    """
    decorator to register a deserializer.

    :param object args: deserializer class constructor arguments.
    :param object kwargs: deserializer class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           deserializer with the same name and accepted type,
                           replace it with the new one, otherwise raise
                           an error. defaults to False.

    :raises CoreTypeError: core type error.

    :returns: deserializer class.

    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available deserializer.

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

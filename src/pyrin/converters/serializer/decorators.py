# -*- coding: utf-8 -*-
"""
serializer decorators module.
"""

import pyrin.converters.serializer.services as serializer_services


def serializer(*args, **kwargs):
    """
    decorator to register a serializer.

    :param object args: serializer class constructor arguments.
    :param object kwargs: serializer class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           serializer with the same accepted type,
                           replace it with the new one, otherwise raise
                           an error. defaults to False.

    :raises InvalidSerializerTypeError: invalid serializer type error.
    :raises DuplicatedSerializerError: duplicated serializer error.

    :returns: serializer class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available serializers.

        :param type cls: serializer class.

        :returns: serializer class.
        :rtype: type
        """

        instance = cls(*args, **kwargs)
        serializer_services.register_serializer(instance, **kwargs)

        return cls

    return decorator

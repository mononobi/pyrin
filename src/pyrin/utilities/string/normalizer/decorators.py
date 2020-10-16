# -*- coding: utf-8 -*-
"""
string normalizer decorators module.
"""

import pyrin.utilities.string.normalizer.services as normalizer_services


def string_normalizer(*args, **kwargs):
    """
    decorator to register a string normalizer.

    :param object args: normalizer class constructor arguments.
    :param object kwargs: normalizer class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           normalizer with the same name, replace it with
                           the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidStringNormalizerTypeError: invalid string normalizer type error.
    :raises DuplicatedStringNormalizerError: duplicated string normalizer error.

    :returns: string normalizer class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available string normalizers.

        :param type cls: normalizer class.

        :returns: normalizer class.
        :rtype: type
        """

        instance = cls(*args, **kwargs)
        normalizer_services.register_normalizer(instance, **kwargs)

        return cls

    return decorator

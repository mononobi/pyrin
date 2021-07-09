# -*- coding: utf-8 -*-
"""
swagger decorators module.
"""

import pyrin.api.swagger.services as swagger_services


def tag(*args, **kwargs):
    """
    decorator to register a tag.

    :param object args: tag class constructor arguments.
    :param object kwargs: tag class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           tag with the same name, replace it with the
                           new one, otherwise raise an error. defaults to False.

    :raises InvalidTagTypeError: invalid tag type error.
    :raises DuplicatedTagError: duplicated tag error.

    :returns: tag class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available tags.

        :param type cls: tag class.

        :returns: tag class.
        :rtype: type
        """

        instance = cls(*args, **kwargs)
        swagger_services.register_tag(instance, **kwargs)

        return cls

    return decorator

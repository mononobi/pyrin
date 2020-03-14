# -*- coding: utf-8 -*-
"""
packaging decorators module.
"""

import pyrin.packaging.services as packaging_services


def packaging_hook():
    """
    decorator to register a packaging hook.

    :raises InvalidPackagingHookTypeError: invalid packaging hook type error.

    :returns: packaging hook class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available packaging hooks.

        :param type cls: packaging hook class.

        :returns: packaging hook class.
        :rtype: type
        """

        instance = cls()
        packaging_services.register_hook(instance)

        return cls

    return decorator

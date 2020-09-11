# -*- coding: utf-8 -*-
"""
api decorators module.
"""

import pyrin.api.services as api_services


def api_hook():
    """
    decorator to register an api hook.

    :raises InvalidAPIHookTypeError: invalid api hook type error.

    :returns: api hook class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available api hooks.

        :param type cls: api hook class.

        :returns: api hook class.
        :rtype: type
        """

        instance = cls()
        api_services.register_hook(instance)

        return cls

    return decorator

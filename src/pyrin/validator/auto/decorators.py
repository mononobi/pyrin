# -*- coding: utf-8 -*-
"""
validator auto decorators module.
"""

import pyrin.validator.auto.services as auto_validator_services


def auto_validator_hook():
    """
    decorator to register an auto validator hook.

    :raises InvalidAutoValidatorHookTypeError: invalid auto validator hook type error.

    :returns: auto validator hook class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available auto validator hooks.

        :param type cls: auto validator hook class.

        :returns: auto validator hook class.
        :rtype: type
        """

        instance = cls()
        auto_validator_services.register_hook(instance)

        return cls

    return decorator

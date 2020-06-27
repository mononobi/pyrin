# -*- coding: utf-8 -*-
"""
validator decorators module.
"""

import pyrin.validator.services as validator_services


def validator(*args, **kwargs):
    """
    decorator to register a validator.

    :param object args: validator class constructor arguments.
    :param object kwargs: validator class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           validator with the same name and domain, replace
                           it with the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidValidatorTypeError: invalid validator type error.
    :raises DuplicatedValidatorError: duplicated validator error.

    :returns: validator class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available validator.

        :param type cls: validator class.

        :returns: validator class.
        :rtype: type
        """

        instance = cls(*args, **kwargs)
        validator_services.register_validator(instance, **kwargs)

        return cls

    return decorator

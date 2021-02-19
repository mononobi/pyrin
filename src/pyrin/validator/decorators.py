# -*- coding: utf-8 -*-
"""
validator decorators module.
"""

import pyrin.validator.services as validator_services


def validator(domain, field, *args, **kwargs):
    """
    decorator to register a validator.

    :param type[BaseEntity] | str domain: the domain in which this validator
                                          must be registered. it could be a
                                          type of a BaseEntity subclass.
                                          if a validator must be registered
                                          independent from any BaseEntity subclass,
                                          the domain could be a unique string name.
                                          note that the provided string name must be
                                          unique at application level.

    :param InstrumentedAttribute | str field: validator field name. it could be a
                                              string or a column. each validator will
                                              be registered with its field name in
                                              corresponding domain. to enable automatic
                                              validations, the provided field name must
                                              be the exact name of the parameter which
                                              this validator will validate. if you pass
                                              a column attribute, some constraints
                                              such as `nullable`, `min_length`, `max_length`,
                                              `min_value`, `max_value`, `allow_blank` and
                                              `allow_whitespace` could be extracted
                                              automatically from that column if not provided
                                              in inputs.

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

        instance = cls(domain, field, *args, **kwargs)
        validator_services.register_validator(instance, **kwargs)

        return cls

    return decorator

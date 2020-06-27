# -*- coding: utf-8 -*-
"""
validator handlers number module.
"""

from pyrin.validator.handlers.base import ValidatorBase


class NumberValidator(ValidatorBase):
    """
    number validator class.
    """

    def __init__(self, domain, name, **options):
        """
        initializes an instance of NumberValidator.

        :param type[BaseEntity] | str domain: the domain in which this validator
                                              must be registered. it could be a
                                              type of a BaseEntity subclass.
                                              if a validator must be registered
                                              independent from any BaseEntity subclass,
                                              the domain could be a unique string name.
                                              note that the provided string name must be
                                              unique at application level.

        :param str name: validator name.
                         each validator will be registered with its name
                         in corresponding domain.
                         to enable automatic validations, the provided
                         name must be the exact name of the parameter
                         which this validator will validate.

        :keyword bool nullable: specifies that null values should be accepted as valid.
                                defaults to True if not provided.

        :keyword str localized_name: localized name of the parameter
                                     which this validator will validate.
                                     it must be passed using `_` method
                                     from `pyrin.core.globals`.
                                     defaults to `name` if not provided.

        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        """

        options.update(accepted_type=(int, float))
        super().__init__(domain, name, **options)


class IntegerValidator(ValidatorBase):
    """
    integer validator class.
    """

    def __init__(self, domain, name, **options):
        """
        initializes an instance of IntegerValidator.

        :param type[BaseEntity] | str domain: the domain in which this validator
                                              must be registered. it could be a
                                              type of a BaseEntity subclass.
                                              if a validator must be registered
                                              independent from any BaseEntity subclass,
                                              the domain could be a unique string name.
                                              note that the provided string name must be
                                              unique at application level.

        :param str name: validator name.
                         each validator will be registered with its name
                         in corresponding domain.
                         to enable automatic validations, the provided
                         name must be the exact name of the parameter
                         which this validator will validate.

        :keyword bool nullable: specifies that null values should be accepted as valid.
                                defaults to True if not provided.

        :keyword str localized_name: localized name of the parameter
                                     which this validator will validate.
                                     it must be passed using `_` method
                                     from `pyrin.core.globals`.
                                     defaults to `name` if not provided.

        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        """

        options.update(accepted_type=int)
        super().__init__(domain, name, **options)


class FloatValidator(ValidatorBase):
    """
    float validator class.
    """

    def __init__(self, domain, name, **options):
        """
        initializes an instance of FloatValidator.

        :param type[BaseEntity] | str domain: the domain in which this validator
                                              must be registered. it could be a
                                              type of a BaseEntity subclass.
                                              if a validator must be registered
                                              independent from any BaseEntity subclass,
                                              the domain could be a unique string name.
                                              note that the provided string name must be
                                              unique at application level.

        :param str name: validator name.
                         each validator will be registered with its name
                         in corresponding domain.
                         to enable automatic validations, the provided
                         name must be the exact name of the parameter
                         which this validator will validate.

        :keyword bool nullable: specifies that null values should be accepted as valid.
                                defaults to True if not provided.

        :keyword str localized_name: localized name of the parameter
                                     which this validator will validate.
                                     it must be passed using `_` method
                                     from `pyrin.core.globals`.
                                     defaults to `name` if not provided.

        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        """

        options.update(accepted_type=float)
        super().__init__(domain, name, **options)

# -*- coding: utf-8 -*-
"""
validator handlers datetime module.
"""

from datetime import datetime, date, time

from pyrin.validator.handlers.base import ValidatorBase


class DateTimeValidator(ValidatorBase):
    """
    datetime validator class.
    """

    def __init__(self, domain, name, **options):
        """
        initializes an instance of DateTimeValidator.

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

        options.update(accepted_type=datetime)
        super().__init__(domain, name, **options)


class DateValidator(ValidatorBase):
    """
    date validator class.
    """

    def __init__(self, domain, name, **options):
        """
        initializes an instance of DateValidator.

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

        options.update(accepted_type=date)
        super().__init__(domain, name, **options)


class TimeValidator(ValidatorBase):
    """
    time validator class.
    """

    def __init__(self, domain, name, **options):
        """
        initializes an instance of TimeValidator.

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

        options.update(accepted_type=time)
        super().__init__(domain, name, **options)

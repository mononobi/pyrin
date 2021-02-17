# -*- coding: utf-8 -*-
"""
validator handlers datetime module.
"""

from datetime import datetime, date, time

import pyrin.globalization.datetime.services as datetime_services

from pyrin.core.globals import _
from pyrin.validator.handlers.base import ValidatorBase
from pyrin.validator.handlers.exceptions import ValueIsNotDateTimeError, ValueIsNotDateError, \
    ValueIsNotTimeError


class DateTimeValidator(ValidatorBase):
    """
    datetime validator class.
    """

    invalid_type_error = ValueIsNotDateTimeError
    invalid_type_message = _('The provided value for [{param_name}] '
                             'must be a datetime.')

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

        :keyword bool is_list: specifies that the value must be a list of items.
                               defaults to False if not provided.

        :keyword bool null_items: specifies that list items could be None.
                                  it is only used if `is_list=True` is provided.
                                  defaults to False if not provided.

        :keyword bool allow_single: specifies that list validator should also
                                    accept single, non list values.
                                    it is only used if `is_list=True` is provided.
                                    defaults to False if not provided.

        :keyword bool allow_empty_list: specifies that list validators should also
                                        accept empty lists.
                                        it is only used if `is_list=True` is provided.
                                        defaults to False if not provided.

        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises ValidatorFixerMustBeCallable: validator fixer must be callable.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        """

        options.update(accepted_type=datetime)
        super().__init__(domain, name, **options)

    def _get_safe_representation(self, value):
        """
        gets the string representable version of input value.

        :param datetime value: value to get its string representation.

        :returns: string representable value.
        :rtype: str
        """

        return datetime_services.to_datetime_string(value, server=False)


class DateValidator(ValidatorBase):
    """
    date validator class.
    """

    invalid_type_error = ValueIsNotDateError
    invalid_type_message = _('The provided value for [{param_name}] '
                             'must be a date.')

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

        :keyword bool is_list: specifies that the value must be a list of items.
                               defaults to False if not provided.

        :keyword bool null_items: specifies that list items could be None.
                                  it is only used if `is_list=True` is provided.
                                  defaults to False if not provided.

        :keyword bool allow_single: specifies that list validator should also
                                    accept single, non list values.
                                    it is only used if `is_list=True` is provided.
                                    defaults to False if not provided.

        :keyword bool allow_empty_list: specifies that list validators should also
                                        accept empty lists.
                                        it is only used if `is_list=True` is provided.
                                        defaults to False if not provided.

        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises ValidatorFixerMustBeCallable: validator fixer must be callable.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        """

        options.update(accepted_type=date)
        super().__init__(domain, name, **options)

    def _get_safe_representation(self, value):
        """
        gets the string representable version of input value.

        :param date value: value to get its string representation.

        :returns: string representable value.
        :rtype: str
        """

        return datetime_services.to_date_string(value)


class TimeValidator(ValidatorBase):
    """
    time validator class.
    """

    invalid_type_error = ValueIsNotTimeError
    invalid_type_message = _('The provided value for [{param_name}] '
                             'must be a time.')

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

        :keyword bool is_list: specifies that the value must be a list of items.
                               defaults to False if not provided.

        :keyword bool null_items: specifies that list items could be None.
                                  it is only used if `is_list=True` is provided.
                                  defaults to False if not provided.

        :keyword bool allow_single: specifies that list validator should also
                                    accept single, non list values.
                                    it is only used if `is_list=True` is provided.
                                    defaults to False if not provided.

        :keyword bool allow_empty_list: specifies that list validators should also
                                        accept empty lists.
                                        it is only used if `is_list=True` is provided.
                                        defaults to False if not provided.

        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises ValidatorFixerMustBeCallable: validator fixer must be callable.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        """

        options.update(accepted_type=time)
        super().__init__(domain, name, **options)

    def _get_safe_representation(self, value):
        """
        gets the string representable version of input value.

        :param time value: value to get its string representation.

        :returns: string representable value.
        :rtype: str
        """

        return datetime_services.to_time_string(value, server=False)

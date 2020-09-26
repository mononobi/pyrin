# -*- coding: utf-8 -*-
"""
validator handlers misc module.
"""

from pyrin.core.globals import _, LIST_TYPES
from pyrin.validator.handlers.base import ValidatorBase
from pyrin.validator.handlers.exceptions import ValueIsLowerThanMinimumError, \
    ValueIsHigherThanMaximumError, ValueIsOutOfRangeError, \
    AcceptedMinimumValueMustBeProvidedError, AcceptedMaximumValueMustBeProvidedError, \
    ValidValuesMustBeProvidedError, InvalidValuesMustBeProvidedError, \
    MinimumValueLargerThanMaximumValueError


class MinimumValidator(ValidatorBase):
    """
    minimum validator class.
    """

    minimum_value_error = ValueIsLowerThanMinimumError
    minimum_value_message = _('The provided value for [{param_name}] must '
                              'be greater than {or_equal}[{minimum}].')

    inclusive_minimum_value_message = _('or equal to ')

    default_accepted_minimum = None
    default_inclusive_minimum = None

    def __init__(self, domain, name, **options):
        """
        initializes an instance of MinimumValidator.

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

        :keyword type | tuple[type] accepted_type: accepted type for value.
                                                   no type checking will be
                                                   done if not provided.

        :keyword bool nullable: specifies that null values should be accepted as valid.
                                defaults to True if not provided.

        :keyword str localized_name: localized name of the parameter
                                     which this validator will validate.
                                     it must be passed using `_` method
                                     from `pyrin.core.globals`.
                                     defaults to `name` if not provided.

        :keyword object accepted_minimum: the lower bound of values that
                                          this validator considers valid.

        :keyword bool inclusive_minimum: determines that values equal to
                                         accepted minimum should be considered valid.
                                         this value has precedence over `inclusive_minimum`
                                         instance attribute if provided.

        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidAcceptedTypeError: invalid accepted type error.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        :raises AcceptedMinimumValueMustBeProvidedError: accepted minimum value
                                                         must be provided error.
        """

        super().__init__(domain, name, **options)

        inclusive_minimum = options.get('inclusive_minimum')
        if inclusive_minimum is None:
            if self.default_inclusive_minimum is not None:
                inclusive_minimum = self.default_inclusive_minimum
            else:
                inclusive_minimum = True

        accepted_minimum = options.get('accepted_minimum')
        if accepted_minimum is None:
            if self.default_accepted_minimum is not None:
                accepted_minimum = self.default_accepted_minimum
            else:
                raise AcceptedMinimumValueMustBeProvidedError('Accepted minimum value '
                                                              'could not be None.')

        self._accepted_minimum = accepted_minimum
        self._inclusive_minimum = inclusive_minimum

        self._validate_exception_type(self.minimum_value_error)

    def _validate(self, value, **options):
        """
        validates the given value.

        it raises an error if validation fails.
        the raised error must be an instance of ValidationError.
        each overridden method must call `super()._validate()`
        preferably at the beginning.

        :param object value: value to be validated.

        :keyword bool inclusive_minimum: determines that values equal to
                                         accepted minimum should be considered valid.
                                         this value has precedence over `inclusive_minimum`
                                         instance attribute if provided.

        :raises ValueIsLowerThanMinimumError: value is lower than minimum error.
        """

        super()._validate(value, **options)

        inclusive_minimum = options.get('inclusive_minimum')
        if inclusive_minimum is None:
            inclusive_minimum = self.inclusive_minimum

        if value < self.accepted_minimum or \
                (value == self.accepted_minimum and inclusive_minimum is False):
            equality = ''
            if inclusive_minimum is not False:
                equality = self.inclusive_minimum_value_message

            raise self.minimum_value_error(
                self.minimum_value_message.format(param_name=self.localized_name,
                                                  minimum=self.accepted_minimum,
                                                  or_equal=equality))

    @property
    def accepted_minimum(self):
        """
        gets the lower bound of values that this validator considers valid.

        :rtype: object
        """

        return self._accepted_minimum

    @property
    def inclusive_minimum(self):
        """
        gets a value indicating that values equal to accepted minimum must be considered valid.

        :rtype: bool
        """

        return self._inclusive_minimum


class MaximumValidator(ValidatorBase):
    """
    maximum validator class.
    """

    maximum_value_error = ValueIsHigherThanMaximumError
    maximum_value_message = _('The provided value for [{param_name}] must '
                              'be lower than {or_equal}[{maximum}].')

    inclusive_maximum_value_message = _('or equal to ')

    default_inclusive_maximum = None
    default_accepted_maximum = None

    def __init__(self, domain, name, **options):
        """
        initializes an instance of MaximumValidator.

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

        :keyword type | tuple[type] accepted_type: accepted type for value.
                                                   no type checking will be
                                                   done if not provided.

        :keyword bool nullable: specifies that null values should be accepted as valid.
                                defaults to True if not provided.

        :keyword str localized_name: localized name of the parameter
                                     which this validator will validate.
                                     it must be passed using `_` method
                                     from `pyrin.core.globals`.
                                     defaults to `name` if not provided.

        :keyword object accepted_maximum: the upper bound of values that
                                          this validator considers valid.

        :keyword bool inclusive_maximum: determines that values equal to
                                         accepted maximum should be considered valid.
                                         this value has precedence over `inclusive_maximum`
                                         instance attribute if provided.

        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidAcceptedTypeError: invalid accepted type error.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        :raises AcceptedMaximumValueMustBeProvidedError: accepted maximum value
                                                         must be provided error.
        """

        super().__init__(domain, name, **options)

        inclusive_maximum = options.get('inclusive_maximum')
        if inclusive_maximum is None:
            if self.default_inclusive_maximum is not None:
                inclusive_maximum = self.default_inclusive_maximum
            else:
                inclusive_maximum = True

        accepted_maximum = options.get('accepted_maximum')
        if accepted_maximum is None:
            if self.default_accepted_maximum is not None:
                accepted_maximum = self.default_accepted_maximum
            else:
                raise AcceptedMaximumValueMustBeProvidedError('Accepted maximum value '
                                                              'could not be None.')

        self._accepted_maximum = accepted_maximum
        self._inclusive_maximum = inclusive_maximum

        self._validate_exception_type(self.maximum_value_error)

    def _validate(self, value, **options):
        """
        validates the given value.

        it raises an error if validation fails.
        the raised error must be an instance of ValidationError.
        each overridden method must call `super()._validate()`
        preferably at the beginning.

        :param object value: value to be validated.

        :keyword bool inclusive_maximum: determines that values equal to
                                         accepted maximum should be considered valid.
                                         this value has precedence over `inclusive_maximum`
                                         instance attribute if provided.

        :raises ValueIsHigherThanMaximumError: value is higher than maximum error.
        """

        super()._validate(value, **options)

        inclusive_maximum = options.get('inclusive_maximum')
        if inclusive_maximum is None:
            inclusive_maximum = self.inclusive_maximum

        if value > self.accepted_maximum or \
                (value == self.accepted_maximum and inclusive_maximum is False):
            equality = ''
            if inclusive_maximum is not False:
                equality = self.inclusive_maximum_value_message

            raise self.maximum_value_error(
                self.maximum_value_message.format(param_name=self.localized_name,
                                                  maximum=self.accepted_maximum,
                                                  or_equal=equality))

    @property
    def accepted_maximum(self):
        """
        gets the upper bound of values that this validator considers valid.

        :rtype: object
        """

        return self._accepted_maximum

    @property
    def inclusive_maximum(self):
        """
        gets a value indicating that values equal to accepted maximum must be considered valid.

        :rtype: bool
        """

        return self._inclusive_maximum


class RangeValidator(MinimumValidator, MaximumValidator):
    """
    range validator class.
    """

    range_value_error = ValueIsOutOfRangeError
    range_value_message = _('The provided value for [{param_name}] must '
                            'be greater than {or_equal_min}[{lower}] and '
                            'lower than {or_equal_max}[{upper}].')

    def __init__(self, domain, name, **options):
        """
        initializes an instance of RangeValidator.

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

        :keyword type | tuple[type] accepted_type: accepted type for value.
                                                   no type checking will be
                                                   done if not provided.

        :keyword bool nullable: specifies that null values should be accepted as valid.
                                defaults to True if not provided.

        :keyword str localized_name: localized name of the parameter
                                     which this validator will validate.
                                     it must be passed using `_` method
                                     from `pyrin.core.globals`.
                                     defaults to `name` if not provided.

        :keyword object accepted_minimum: the lower bound of values that
                                          this validator considers valid.

        :keyword bool inclusive_minimum: determines that values equal to
                                         accepted minimum should be considered valid.
                                         this value has precedence over `inclusive_minimum`
                                         instance attribute if provided.

        :keyword object accepted_maximum: the upper bound of values that
                                          this validator considers valid.

        :keyword bool inclusive_maximum: determines that values equal to
                                         accepted maximum should be considered valid.
                                         this value has precedence over `inclusive_maximum`
                                         instance attribute if provided.

        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidAcceptedTypeError: invalid accepted type error.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        :raises AcceptedMinimumValueMustBeProvidedError: accepted minimum value
                                                         must be provided error.
        :raises AcceptedMaximumValueMustBeProvidedError: accepted maximum value
                                                         must be provided error.
        :raises MinimumValueLargerThanMaximumValueError: minimum value larger
                                                         than maximum value error.
        """

        super().__init__(domain, name, **options)

        if self.accepted_minimum is not None and self.accepted_maximum is not None \
                and self.accepted_minimum > self.accepted_maximum:
            raise MinimumValueLargerThanMaximumValueError('Accepted minimum value could not be '
                                                          'larger than accepted maximum value.')

        self._validate_exception_type(self.range_value_error)

    def _validate(self, value, **options):
        """
        validates the given value.

        it raises an error if validation fails.
        the raised error must be an instance of ValidationError.
        each overridden method must call `super()._validate()`
        preferably at the beginning.

        :param object value: value to be validated.

        :keyword bool inclusive_minimum: determines that values equal to
                                         accepted minimum should be considered valid.
                                         this value has precedence over `inclusive_minimum`
                                         instance attribute if provided.

        :keyword bool inclusive_maximum: determines that values equal to
                                         accepted maximum should be considered valid.
                                         this value has precedence over `inclusive_maximum`
                                         instance attribute if provided.

        :raises ValueIsOutOfRangeError: value is out of range error.
        """

        try:
            super()._validate(value, **options)
        except (self.maximum_value_error, self.minimum_value_error):
            equality_min = ''
            equality_max = ''

            inclusive_maximum = options.get('inclusive_maximum')
            if inclusive_maximum is None:
                inclusive_maximum = self.inclusive_maximum

            inclusive_minimum = options.get('inclusive_minimum')
            if inclusive_minimum is None:
                inclusive_minimum = self.inclusive_minimum

            if inclusive_minimum is not False:
                equality_min = self.inclusive_minimum_value_message

            if inclusive_maximum is not False:
                equality_max = self.inclusive_maximum_value_message

            raise self.range_value_error(self.range_value_message.format(
                param_name=self.localized_name,
                lower=self.accepted_minimum, upper=self.accepted_maximum,
                or_equal_min=equality_min, or_equal_max=equality_max))


class InValidator(ValidatorBase):
    """
    in validator class.
    """

    not_in_value_error = ValueIsOutOfRangeError
    not_in_value_message = _('The provided value for [{param_name}] '
                             'must be from [{values}].')

    def __init__(self, domain, name, **options):
        """
        initializes an instance of InValidator.

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

        :keyword type | tuple[type] accepted_type: accepted type for value.
                                                   no type checking will be
                                                   done if not provided.

        :keyword bool nullable: specifies that null values should be accepted as valid.
                                defaults to True if not provided.

        :keyword str localized_name: localized name of the parameter
                                     which this validator will validate.
                                     it must be passed using `_` method
                                     from `pyrin.core.globals`.
                                     defaults to `name` if not provided.

        :keyword list[object] valid_values: a list of valid values.

        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidAcceptedTypeError: invalid accepted type error.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        :raises ValidValuesMustBeProvidedError: valid values must be provided error.
        """

        super().__init__(domain, name, **options)

        valid_values = options.get('valid_values')
        if valid_values is None or not \
                isinstance(valid_values, LIST_TYPES) or len(valid_values) <= 0:
            raise ValidValuesMustBeProvidedError('Valid values must be provided as iterable.')

        self._valid_values = valid_values
        self._validate_exception_type(self.not_in_value_error)

    def _validate(self, value, **options):
        """
        validates the given value.

        it raises an error if validation fails.
        the raised error must be an instance of ValidationError.
        each overridden method must call `super()._validate()`
        preferably at the beginning.

        :param object value: value to be validated.

        :raises ValueIsOutOfRangeError: value is out of range error.
        """

        super()._validate(value, **options)

        if value not in self.valid_values:
            raise self.not_in_value_error(self.not_in_value_message.format(
                param_name=self.localized_name, values=self.valid_values))

    @property
    def valid_values(self):
        """
        gets a list of valid values for this validator.

        :rtype: list[object]
        """

        return self._valid_values


class NotInValidator(ValidatorBase):
    """
    not in validator class.
    """

    in_value_error = ValueIsOutOfRangeError
    in_value_message = _('The provided value for [{param_name}] '
                         'could not be from [{values}].')

    def __init__(self, domain, name, **options):
        """
        initializes an instance of NotInValidator.

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

        :keyword type | tuple[type] accepted_type: accepted type for value.
                                                   no type checking will be
                                                   done if not provided.

        :keyword bool nullable: specifies that null values should be accepted as valid.
                                defaults to True if not provided.

        :keyword str localized_name: localized name of the parameter
                                     which this validator will validate.
                                     it must be passed using `_` method
                                     from `pyrin.core.globals`.
                                     defaults to `name` if not provided.

        :keyword list[object] invalid_values: a list of invalid values.

        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidAcceptedTypeError: invalid accepted type error.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        :raises InvalidValuesMustBeProvidedError: invalid values must be provided error.
        """

        super().__init__(domain, name, **options)

        invalid_values = options.get('invalid_values')
        if invalid_values is None or not \
                isinstance(invalid_values, LIST_TYPES) or len(invalid_values) <= 0:
            raise InvalidValuesMustBeProvidedError('Invalid values must be '
                                                   'provided as iterable.')

        self._invalid_values = invalid_values
        self._validate_exception_type(self.in_value_error)

    def _validate(self, value, **options):
        """
        validates the given value.

        it raises an error if validation fails.
        the raised error must be an instance of ValidationError.
        each overridden method must call `super()._validate()`
        preferably at the beginning.

        :param object value: value to be validated.

        :raises ValueIsOutOfRangeError: value is out of range error.
        """

        super()._validate(value, **options)

        if value in self.invalid_values:
            raise self.in_value_error(self.in_value_message.format(
                param_name=self.localized_name, values=self.invalid_values))

    @property
    def invalid_values(self):
        """
        gets a list of invalid values for this validator.

        :rtype: list[object]
        """

        return self._invalid_values

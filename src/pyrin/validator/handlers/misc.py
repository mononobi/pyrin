# -*- coding: utf-8 -*-
"""
validator handlers misc module.
"""

from pyrin.core.globals import _, LIST_TYPES
from pyrin.core.decorators import class_property
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

    # accepted minimum value, it could also be a callable without any inputs.
    default_accepted_minimum = None
    default_inclusive_minimum = None

    def __init__(self, domain, field, **options):
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

        :param InstrumentedAttribute | str field: validator field name. it could be a
                                                  string or a column. each validator will
                                                  be registered with its field name in
                                                  corresponding domain. to enable automatic
                                                  validations, the provided field name must
                                                  be the exact name of the parameter which
                                                  this validator will validate. if you pass
                                                  a column attribute, some constraints
                                                  such as `nullable`, `min_length`, `max_length`,
                                                  `min_value`, `max_value`, `allow_blank`,
                                                  `allow_whitespace`, `check_in` and
                                                  `check_not_in` could be extracted
                                                  automatically from that column if not provided
                                                  in inputs.

        :keyword type | tuple[type] accepted_type: accepted type for value.
                                                   no type checking will be
                                                   done if not provided.

        :keyword type | tuple[type] not_accepted_type: not accepted type for value.
                                                       it is useful to provide both
                                                       `accepted_type` and `not_accepted_type`
                                                       when you want to separate two types
                                                       which, one of them is a subclass
                                                       of the other. for example `datetime`
                                                       and `date` or `bool` and `int`.
                                                       note that if `accepted_type` is
                                                       not provided, this value has no effect.

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

        :keyword str name: a custom name for this validator.
                           if provided, the name of `field` will be ignored.

        :keyword bool for_find: specifies that this validator must only
                                be used on validation for find.
                                defaults to False if not provided.

        :keyword bool inclusive_minimum: determines that values equal to
                                         accepted minimum should be considered valid.
                                         this value has precedence over `inclusive_minimum`
                                         instance attribute if provided.

        :raises ValidatorFieldIsRequiredError: validator field is required error.
        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidAcceptedTypeError: invalid accepted type error.
        :raises InvalidNotAcceptedTypeError: invalid not accepted type error.
        :raises ValidatorFixerMustBeCallable: validator fixer must be callable.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        :raises AcceptedMinimumValueMustBeProvidedError: accepted minimum value
                                                         must be provided error.
        """

        super().__init__(domain, field, **options)

        inclusive_minimum = options.get('inclusive_minimum')
        if inclusive_minimum is None:
            if self.default_inclusive_minimum is not None:
                inclusive_minimum = self.default_inclusive_minimum
            else:
                inclusive_minimum = True

        if self.default_accepted_minimum is None and \
                (self.field is None or self.field.min_value is None):
            raise AcceptedMinimumValueMustBeProvidedError('Accepted minimum value for '
                                                          'validator [{name}] could not '
                                                          'be None.'.format(name=self))

        self._inclusive_minimum = inclusive_minimum
        self._instance_accepted_minimum = None
        if self.default_accepted_minimum is None:
            self._instance_accepted_minimum = self.field.min_value

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

        current_min = self.accepted_minimum
        current_values = options.get(RangeValidator.CURRENT_VALUE_KEY)
        if current_values is not None:
            current_values[RangeValidator.CURRENT_MIN_KEY] = current_min

        if value < current_min or (value == current_min and inclusive_minimum is False):
            equality = ''
            if inclusive_minimum is not False:
                equality = self.inclusive_minimum_value_message

            raise self.minimum_value_error(
                self.minimum_value_message.format(param_name=self.localized_name,
                                                  minimum=
                                                  self._get_representation(current_min),
                                                  or_equal=equality))

    @property
    def accepted_minimum(self):
        """
        gets the lower bound of values that this validator considers valid.

        :rtype: object
        """

        return self._get_value(self.accepted_minimum_provider)

    @property
    def inclusive_minimum(self):
        """
        gets a value indicating that values equal to accepted minimum must be considered valid.

        :rtype: bool
        """

        return self._inclusive_minimum

    @property
    def instance_accepted_minimum(self):
        """
        gets the instance accepted minimum.

        :rtype: object | callable
        """

        return self._instance_accepted_minimum

    @class_property
    def class_accepted_minimum(cls):
        """
        gets the class accepted minimum.

        :rtype: object | callable
        """

        return cls.default_accepted_minimum

    @property
    def accepted_minimum_provider(self):
        """
        gets the accepted minimum provider of this instance.

        it may be a class level or instance level object or callable.
        it may also be None.

        :rtype: object | callable
        """

        if self.instance_accepted_minimum is not None:
            return self.instance_accepted_minimum

        if self.class_accepted_minimum is not None:
            return self.class_accepted_minimum

        return None


class MaximumValidator(ValidatorBase):
    """
    maximum validator class.
    """

    maximum_value_error = ValueIsHigherThanMaximumError
    maximum_value_message = _('The provided value for [{param_name}] must '
                              'be lower than {or_equal}[{maximum}].')

    inclusive_maximum_value_message = _('or equal to ')

    # accepted maximum value, it could also be a callable without any inputs.
    default_accepted_maximum = None
    default_inclusive_maximum = None

    def __init__(self, domain, field, **options):
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

        :param InstrumentedAttribute | str field: validator field name. it could be a
                                                  string or a column. each validator will
                                                  be registered with its field name in
                                                  corresponding domain. to enable automatic
                                                  validations, the provided field name must
                                                  be the exact name of the parameter which
                                                  this validator will validate. if you pass
                                                  a column attribute, some constraints
                                                  such as `nullable`, `min_length`, `max_length`,
                                                  `min_value`, `max_value`, `allow_blank`,
                                                  `allow_whitespace`, `check_in` and
                                                  `check_not_in` could be extracted
                                                  automatically from that column if not provided
                                                  in inputs.

        :keyword type | tuple[type] accepted_type: accepted type for value.
                                                   no type checking will be
                                                   done if not provided.

        :keyword type | tuple[type] not_accepted_type: not accepted type for value.
                                                       it is useful to provide both
                                                       `accepted_type` and `not_accepted_type`
                                                       when you want to separate two types
                                                       which, one of them is a subclass
                                                       of the other. for example `datetime`
                                                       and `date` or `bool` and `int`.
                                                       note that if `accepted_type` is
                                                       not provided, this value has no effect.

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

        :keyword str name: a custom name for this validator.
                           if provided, the name of `field` will be ignored.

        :keyword bool for_find: specifies that this validator must only
                                be used on validation for find.
                                defaults to False if not provided.

        :keyword bool inclusive_maximum: determines that values equal to
                                         accepted maximum should be considered valid.
                                         this value has precedence over `inclusive_maximum`
                                         instance attribute if provided.

        :raises ValidatorFieldIsRequiredError: validator field is required error.
        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidAcceptedTypeError: invalid accepted type error.
        :raises InvalidNotAcceptedTypeError: invalid not accepted type error.
        :raises ValidatorFixerMustBeCallable: validator fixer must be callable.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        :raises AcceptedMaximumValueMustBeProvidedError: accepted maximum value
                                                         must be provided error.
        """

        super().__init__(domain, field, **options)

        inclusive_maximum = options.get('inclusive_maximum')
        if inclusive_maximum is None:
            if self.default_inclusive_maximum is not None:
                inclusive_maximum = self.default_inclusive_maximum
            else:
                inclusive_maximum = True

        if self.default_accepted_maximum is None and \
                (self.field is None or self.field.max_value is None):
            raise AcceptedMaximumValueMustBeProvidedError('Accepted maximum value for '
                                                          'validator [{name}] could not '
                                                          'be None.'.format(name=self))

        self._inclusive_maximum = inclusive_maximum
        self._instance_accepted_maximum = None
        if self.default_accepted_maximum is None:
            self._instance_accepted_maximum = self.field.max_value

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

        current_max = self.accepted_maximum
        current_values = options.get(RangeValidator.CURRENT_VALUE_KEY)
        if current_values is not None:
            current_values[RangeValidator.CURRENT_MAX_KEY] = current_max

        if value > current_max or (value == current_max and inclusive_maximum is False):
            equality = ''
            if inclusive_maximum is not False:
                equality = self.inclusive_maximum_value_message

            raise self.maximum_value_error(
                self.maximum_value_message.format(param_name=self.localized_name,
                                                  maximum=
                                                  self._get_representation(current_max),
                                                  or_equal=equality))

    @property
    def accepted_maximum(self):
        """
        gets the upper bound of values that this validator considers valid.

        :rtype: object
        """

        return self._get_value(self.accepted_maximum_provider)

    @property
    def inclusive_maximum(self):
        """
        gets a value indicating that values equal to accepted maximum must be considered valid.

        :rtype: bool
        """

        return self._inclusive_maximum

    @property
    def instance_accepted_maximum(self):
        """
        gets the instance accepted maximum.

        :rtype: object | callable
        """

        return self._instance_accepted_maximum

    @class_property
    def class_accepted_maximum(cls):
        """
        gets the class accepted maximum.

        :rtype: object | callable
        """

        return cls.default_accepted_maximum

    @property
    def accepted_maximum_provider(self):
        """
        gets the accepted maximum provider of this instance.

        it may be a class level or instance level object or callable.
        it may also be None.

        :rtype: object | callable
        """

        if self.instance_accepted_maximum is not None:
            return self.instance_accepted_maximum

        if self.class_accepted_maximum is not None:
            return self.class_accepted_maximum

        return None


class RangeValidator(MinimumValidator, MaximumValidator):
    """
    range validator class.
    """

    # these values are used inside minimum, maximum and range validators.
    CURRENT_VALUE_KEY = '__current__'
    CURRENT_MAX_KEY = 'max'
    CURRENT_MIN_KEY = 'min'

    range_value_error = ValueIsOutOfRangeError
    range_value_message = _('The provided value for [{param_name}] must '
                            'be greater than {or_equal_min}[{lower}] and '
                            'lower than {or_equal_max}[{upper}].')

    def __init__(self, domain, field, **options):
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

        :param InstrumentedAttribute | str field: validator field name. it could be a
                                                  string or a column. each validator will
                                                  be registered with its field name in
                                                  corresponding domain. to enable automatic
                                                  validations, the provided field name must
                                                  be the exact name of the parameter which
                                                  this validator will validate. if you pass
                                                  a column attribute, some constraints
                                                  such as `nullable`, `min_length`, `max_length`,
                                                  `min_value`, `max_value`, `allow_blank`,
                                                  `allow_whitespace`, `check_in` and
                                                  `check_not_in` could be extracted
                                                  automatically from that column if not provided
                                                  in inputs.

        :keyword type | tuple[type] accepted_type: accepted type for value.
                                                   no type checking will be
                                                   done if not provided.

        :keyword type | tuple[type] not_accepted_type: not accepted type for value.
                                                       it is useful to provide both
                                                       `accepted_type` and `not_accepted_type`
                                                       when you want to separate two types
                                                       which, one of them is a subclass
                                                       of the other. for example `datetime`
                                                       and `date` or `bool` and `int`.
                                                       note that if `accepted_type` is
                                                       not provided, this value has no effect.

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

        :keyword str name: a custom name for this validator.
                           if provided, the name of `field` will be ignored.

        :keyword bool for_find: specifies that this validator must only
                                be used on validation for find.
                                defaults to False if not provided.

        :keyword bool inclusive_minimum: determines that values equal to
                                         accepted minimum should be considered valid.
                                         this value has precedence over `inclusive_minimum`
                                         instance attribute if provided.

        :keyword bool inclusive_maximum: determines that values equal to
                                         accepted maximum should be considered valid.
                                         this value has precedence over `inclusive_maximum`
                                         instance attribute if provided.

        :raises ValidatorFieldIsRequiredError: validator field is required error.
        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidAcceptedTypeError: invalid accepted type error.
        :raises InvalidNotAcceptedTypeError: invalid not accepted type error.
        :raises ValidatorFixerMustBeCallable: validator fixer must be callable.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        :raises AcceptedMinimumValueMustBeProvidedError: accepted minimum value
                                                         must be provided error.
        :raises AcceptedMaximumValueMustBeProvidedError: accepted maximum value
                                                         must be provided error.
        :raises MinimumValueLargerThanMaximumValueError: minimum value larger
                                                         than maximum value error.
        """

        super().__init__(domain, field, **options)

        if not callable(self.accepted_minimum_provider) and \
                not callable(self.accepted_maximum_provider) and \
                self.accepted_minimum is not None and self.accepted_maximum is not None \
                and self.accepted_minimum > self.accepted_maximum:
            raise MinimumValueLargerThanMaximumValueError('Accepted minimum value for '
                                                          'validator [{name}] could not be '
                                                          'larger than accepted maximum value.'
                                                          .format(name=self))

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

        # this is a workaround to get the correct values of accepted min and max in
        # case they are callable and producing different results on each call.
        current_values = dict()
        current_values[self.CURRENT_MAX_KEY] = None
        current_values[self.CURRENT_MIN_KEY] = None
        options[self.CURRENT_VALUE_KEY] = current_values
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

            current_min = current_values.get(self.CURRENT_MIN_KEY)
            if current_min is None:
                current_min = self.accepted_minimum

            current_max = current_values.get(self.CURRENT_MAX_KEY)
            if current_max is None:
                current_max = self.accepted_maximum

            raise self.range_value_error(self.range_value_message.format(
                param_name=self.localized_name,
                lower=self._get_representation(current_min),
                upper=self._get_representation(current_max),
                or_equal_min=equality_min, or_equal_max=equality_max))


class InValidator(ValidatorBase):
    """
    in validator class.
    """

    not_in_value_error = ValueIsOutOfRangeError
    not_in_value_message = _('The provided value for [{param_name}] '
                             'must be one of {values}.')

    # valid values, it must be an iterable or a callable.
    default_valid_values = None

    def __init__(self, domain, field, **options):
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

        :param InstrumentedAttribute | str field: validator field name. it could be a
                                                  string or a column. each validator will
                                                  be registered with its field name in
                                                  corresponding domain. to enable automatic
                                                  validations, the provided field name must
                                                  be the exact name of the parameter which
                                                  this validator will validate. if you pass
                                                  a column attribute, some constraints
                                                  such as `nullable`, `min_length`, `max_length`,
                                                  `min_value`, `max_value`, `allow_blank`,
                                                  `allow_whitespace`, `check_in` and
                                                  `check_not_in` could be extracted
                                                  automatically from that column if not provided
                                                  in inputs.

        :keyword type | tuple[type] accepted_type: accepted type for value.
                                                   no type checking will be
                                                   done if not provided.

        :keyword type | tuple[type] not_accepted_type: not accepted type for value.
                                                       it is useful to provide both
                                                       `accepted_type` and `not_accepted_type`
                                                       when you want to separate two types
                                                       which, one of them is a subclass
                                                       of the other. for example `datetime`
                                                       and `date` or `bool` and `int`.
                                                       note that if `accepted_type` is
                                                       not provided, this value has no effect.

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

        :keyword str name: a custom name for this validator.
                           if provided, the name of `field` will be ignored.

        :keyword bool for_find: specifies that this validator must only
                                be used on validation for find.
                                defaults to False if not provided.

        :raises ValidatorFieldIsRequiredError: validator field is required error.
        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidAcceptedTypeError: invalid accepted type error.
        :raises InvalidNotAcceptedTypeError: invalid not accepted type error.
        :raises ValidatorFixerMustBeCallable: validator fixer must be callable.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        :raises ValidValuesMustBeProvidedError: valid values must be provided error.
        """

        super().__init__(domain, field, **options)

        self._instance_valid_values = None
        if self.default_valid_values is None \
                and self.field is not None and self.field.check_in is not None:
            self._instance_valid_values = self.field.check_in

        if not callable(self.valid_values_provider) and \
                (self.valid_values_provider is None or
                 not isinstance(self.valid_values_provider, LIST_TYPES) or
                 len(self.valid_values_provider) <= 0):
            raise ValidValuesMustBeProvidedError('Valid values for validator [{name}] must '
                                                 'be provided as iterable or callable.'
                                                 .format(name=self))

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

        current_valid = self.valid_values
        if value not in current_valid:
            raise self.not_in_value_error(self.not_in_value_message.format(
                param_name=self.localized_name,
                values=self._get_list_representation(current_valid)))

    @property
    def valid_values(self):
        """
        gets a list of valid values for this validator.

        :rtype: list[object]
        """

        return self._get_value(self.valid_values_provider)

    @property
    def instance_valid_values(self):
        """
        gets the instance valid values.

        :rtype: object | callable
        """

        return self._instance_valid_values

    @class_property
    def class_valid_values(cls):
        """
        gets the class valid values.

        :rtype: object | callable
        """

        return cls.default_valid_values

    @property
    def valid_values_provider(self):
        """
        gets the valid values provider of this instance.

        it may be a class level or instance level object or callable.
        it may also be None.

        :rtype: object | callable
        """

        if self.instance_valid_values is not None:
            return self.instance_valid_values

        if self.class_valid_values is not None:
            return self.class_valid_values

        return None


class NotInValidator(ValidatorBase):
    """
    not in validator class.
    """

    in_value_error = ValueIsOutOfRangeError
    in_value_message = _('The provided value for [{param_name}] '
                         'could not be one of {values}.')

    # invalid values, it must be an iterable or a callable.
    default_invalid_values = None

    def __init__(self, domain, field, **options):
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

        :param InstrumentedAttribute | str field: validator field name. it could be a
                                                  string or a column. each validator will
                                                  be registered with its field name in
                                                  corresponding domain. to enable automatic
                                                  validations, the provided field name must
                                                  be the exact name of the parameter which
                                                  this validator will validate. if you pass
                                                  a column attribute, some constraints
                                                  such as `nullable`, `min_length`, `max_length`,
                                                  `min_value`, `max_value`, `allow_blank`,
                                                  `allow_whitespace`, `check_in` and
                                                  `check_not_in` could be extracted
                                                  automatically from that column if not provided
                                                  in inputs.

        :keyword type | tuple[type] accepted_type: accepted type for value.
                                                   no type checking will be
                                                   done if not provided.

        :keyword type | tuple[type] not_accepted_type: not accepted type for value.
                                                       it is useful to provide both
                                                       `accepted_type` and `not_accepted_type`
                                                       when you want to separate two types
                                                       which, one of them is a subclass
                                                       of the other. for example `datetime`
                                                       and `date` or `bool` and `int`.
                                                       note that if `accepted_type` is
                                                       not provided, this value has no effect.

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

        :keyword str name: a custom name for this validator.
                           if provided, the name of `field` will be ignored.

        :keyword bool for_find: specifies that this validator must only
                                be used on validation for find.
                                defaults to False if not provided.

        :raises ValidatorFieldIsRequiredError: validator field is required error.
        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidAcceptedTypeError: invalid accepted type error.
        :raises InvalidNotAcceptedTypeError: invalid not accepted type error.
        :raises ValidatorFixerMustBeCallable: validator fixer must be callable.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        :raises InvalidValuesMustBeProvidedError: invalid values must be provided error.
        """

        super().__init__(domain, field, **options)

        self._instance_invalid_values = None
        if self.default_invalid_values is None \
                and self.field is not None and self.field.check_not_in is not None:
            self._instance_invalid_values = self.field.check_not_in

        if not callable(self.invalid_values_provider) and \
                (self.invalid_values_provider is None or
                 not isinstance(self.invalid_values_provider, LIST_TYPES) or
                 len(self.invalid_values_provider) <= 0):
            raise InvalidValuesMustBeProvidedError('Invalid values for validator [{name}] '
                                                   'must be provided as iterable or callable.'
                                                   .format(name=self))

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

        current_invalid = self.invalid_values
        if value in current_invalid:
            raise self.in_value_error(self.in_value_message.format(
                param_name=self.localized_name,
                values=self._get_list_representation(current_invalid)))

    @property
    def invalid_values(self):
        """
        gets a list of invalid values for this validator.

        :rtype: list[object]
        """

        return self._get_value(self.invalid_values_provider)

    @property
    def instance_invalid_values(self):
        """
        gets the instance invalid values.

        :rtype: object | callable
        """

        return self._instance_invalid_values

    @class_property
    def class_invalid_values(cls):
        """
        gets the class invalid values.

        :rtype: object | callable
        """

        return cls.default_invalid_values

    @property
    def invalid_values_provider(self):
        """
        gets the invalid values provider of this instance.

        it may be a class level or instance level object or callable.
        it may also be None.

        :rtype: object | callable
        """

        if self.instance_invalid_values is not None:
            return self.instance_invalid_values

        if self.class_invalid_values is not None:
            return self.class_invalid_values

        return None

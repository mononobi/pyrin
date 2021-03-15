# -*- coding: utf-8 -*-
"""
validator handlers string module.
"""

import re

from sqlalchemy import String

import pyrin.utils.string as string_utils

from pyrin.core.globals import _
from pyrin.database.orm.sql.schema.columns import StringColumn
from pyrin.validator.handlers.base import ValidatorBase
from pyrin.validator.handlers.exceptions import LongStringLengthError, ShortStringLengthError, \
    ValueCouldNotBeBlankError, ValueCouldNotBeWhitespaceError, ValueDoesNotMatchPatternError, \
    InvalidRegularExpressionError, RegularExpressionMustBeProvidedError, ValueIsNotStringError, \
    MinimumLengthHigherThanMaximumLengthError, InvalidEmailError, InvalidIPv4Error, \
    InvalidURLError, InvalidHTTPURLError, InvalidHTTPSURLError


class StringValidator(ValidatorBase):
    """
    string validator class.
    """

    invalid_type_error = ValueIsNotStringError
    invalid_type_message = _('The provided value for [{param_name}] '
                             'must be a string.')
    long_length_error = LongStringLengthError
    long_length_message = _('The provided value for [{param_name}] '
                            'should have at most [{count}] characters.')
    short_length_error = ShortStringLengthError
    short_length_message = _('The provided value for [{param_name}] '
                             'should have at least [{count}] characters.')
    blank_value_error = ValueCouldNotBeBlankError
    blank_value_message = _('The provided value for [{param_name}] '
                            'could not be blank.')
    whitespace_value_error = ValueCouldNotBeWhitespaceError
    whitespace_value_message = _('The provided value for [{param_name}] '
                                 'could not be whitespace.')

    default_allow_blank = None
    default_allow_whitespace = None
    default_minimum_length = None
    default_maximum_length = None
    default_fixer = string_utils.coerce_to_string

    def __init__(self, domain, field, **options):
        """
        initializes an instance of StringValidator.

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

        :keyword bool allow_blank: specifies that empty strings should be accepted
                                   as valid. defaults to False if not provided.

        :keyword bool allow_whitespace: specifies that whitespace strings should be accepted
                                        as valid. defaults to False if not provided.

        :keyword int minimum_length: specifies the minimum valid length for string value.
                                     no min length checking will be done if not provided.

        :keyword int maximum_length: specifies the maximum valid length for string value.
                                     no max length checking will be done if not provided.

        :raises ValidatorFieldIsRequiredError: validator field is required error.
        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidNotAcceptedTypeError: invalid not accepted type error.
        :raises ValidatorFixerMustBeCallable: validator fixer must be callable.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        :raises MinimumLengthHigherThanMaximumLengthError: minimum length higher than
                                                           maximum length error.
        """

        options.update(accepted_type=str)
        super().__init__(domain, field, **options)

        allow_blank = options.get('allow_blank')
        if allow_blank is None:
            if self.default_allow_blank is not None:
                allow_blank = self.default_allow_blank
            elif self.is_string_column and self.field.allow_blank is not None:
                allow_blank = self.field.allow_blank
            else:
                allow_blank = False

        allow_whitespace = options.get('allow_whitespace')
        if allow_whitespace is None:
            if self.default_allow_whitespace is not None:
                allow_whitespace = self.default_allow_whitespace
            elif self.is_string_column and self.field.allow_whitespace is not None:
                allow_whitespace = self.field.allow_whitespace
            else:
                allow_whitespace = False

        self._minimum_length = options.get('minimum_length')
        if self._minimum_length is None:
            if self.default_minimum_length is not None:
                self._minimum_length = self.default_minimum_length
            elif self.is_string_column and self.field.min_length is not None:
                self._minimum_length = self.field.min_length
            elif allow_blank is False:
                self._minimum_length = 1

        self._maximum_length = options.get('maximum_length')
        if self._maximum_length is None:
            if self.default_maximum_length is not None:
                self._maximum_length = self.default_maximum_length
            elif self.is_string_type and self.field.type.length is not None:
                self._maximum_length = self.field.type.length
            elif self.is_string_column and self.field.max_length is not None:
                self._maximum_length = self.field.max_length

        if self._minimum_length is not None and self._maximum_length is not None \
                and self._minimum_length > self._maximum_length:
            raise MinimumLengthHigherThanMaximumLengthError('Minimum length of string for '
                                                            'validator [{name}] could not be '
                                                            'higher than maximum length.'
                                                            .format(name=self))

        self._allow_blank = allow_blank
        self._allow_whitespace = allow_whitespace

        self._validate_exception_type(self.long_length_error)
        self._validate_exception_type(self.short_length_error)
        self._validate_exception_type(self.blank_value_error)
        self._validate_exception_type(self.whitespace_value_error)

    def _validate(self, value, **options):
        """
        validates the given value.

        it raises an error if validation fails.
        the raised error must be an instance of ValidationError.
        each overridden method must call `super()._validate()`
        preferably at the beginning.

        :param str value: value to be validated.

        :keyword bool allow_blank: determines that empty strings should be
                                   considered valid. this value has precedence
                                   over `allow_blank` instance attribute
                                   if provided.

        :keyword bool allow_whitespace: determines that whitespace strings should be
                                        considered valid. this value has precedence
                                        over `allow_whitespace` instance attribute
                                        if provided.

        :raises LongStringLengthError: long string length error.
        :raises ShortStringLengthError: short string length error.
        :raises ValueCouldNotBeBlankError: value could not be blank error.
        :raises ValueCouldNotBeWhitespaceError: value could not be whitespace error.
        """

        super()._validate(value, **options)

        allow_blank = options.get('allow_blank')
        if allow_blank is None:
            allow_blank = self.allow_blank

        allow_whitespace = options.get('allow_whitespace')
        if allow_whitespace is None:
            allow_whitespace = self.allow_whitespace

        length = len(value)
        if self.maximum_length is not None and length > self.maximum_length:
            raise self.long_length_error(self.long_length_message.format(
                param_name=self.localized_name, count=self.maximum_length))

        if self.minimum_length is not None and length < self.minimum_length:
            raise self.short_length_error(self.short_length_message.format(
                param_name=self.localized_name, count=self.minimum_length))

        if allow_blank is not True and length == 0:
            raise self.blank_value_error(self.blank_value_message.format(
                param_name=self.localized_name))

        if allow_whitespace is not True and value.isspace():
            raise self.whitespace_value_error(self.whitespace_value_message.format(
                param_name=self.localized_name))

        if length > 0 and not value.isspace():
            self._validate_extra(value, **options)

    def _validate_extra(self, value, **options):
        """
        validates the given value.

        this method is intended to be overridden by subclasses.
        it raises an error if validation fails.
        the raised error must be an instance of ValidationError.
        each overridden method must call `super()._validate_extra()`
        preferably at the beginning.

        :param str value: value to be validated.

        :raises ValidationError: validation error.
        """
        pass

    @property
    def minimum_length(self):
        """
        gets the minimum accepted length of this validator.

        returns None if no minimum has been set.

        :rtype: int
        """

        return self._minimum_length

    @property
    def maximum_length(self):
        """
        gets the maximum accepted length of this validator.

        returns None if no maximum has been set.

        :rtype: int
        """

        return self._maximum_length

    @property
    def allow_blank(self):
        """
        gets a value indicating that empty strings are considered valid.

        :rtype: bool
        """

        return self._allow_blank

    @property
    def allow_whitespace(self):
        """
        gets a value indicating that whitespace strings are considered valid.

        :rtype: bool
        """

        return self._allow_whitespace

    @property
    def is_string_type(self):
        """
        gets a value indicating that the field type of this validator is sqlalchemy `String`.

        :rtype: bool
        """

        return self.field is not None and isinstance(self.field.type, String)

    @property
    def is_string_column(self):
        """
        gets a value indicating that the field column type of this validator is `StringColumn`.

        :rtype: bool
        """

        return isinstance(self.column, StringColumn)


class RegexValidator(StringValidator):
    """
    regex validator class.
    """

    # the regular expression to use for validation.
    # it could be set with a string containing a regex
    # or with a `Pattern` object from re.compile() method.
    regex = None
    pattern_not_match_error = ValueDoesNotMatchPatternError
    pattern_not_match_message = _('The provided value for [{param_name}] '
                                  'does not match the required pattern.')

    default_flags = re.IGNORECASE | re.DOTALL

    def __init__(self, domain, field, **options):
        """
        initializes an instance of RegexValidator.

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

        :keyword bool allow_blank: specifies that empty strings should be accepted
                                   as valid. defaults to False if not provided.

        :keyword bool allow_whitespace: specifies that whitespace strings should be accepted
                                        as valid. defaults to False if not provided.

        :keyword int minimum_length: specifies the minimum valid length for string value.
                                     no min length checking will be done if not provided.

        :keyword int maximum_length: specifies the maximum valid length for string value.
                                     no max length checking will be done if not provided.

        :keyword int flags: flags to be used for regular expression
                            compilation using `re.compile` method.
                            this will only be used if a string regex is provided.
                            if no flags are provided, `default_flags` will be applied.

        :raises ValidatorFieldIsRequiredError: validator field is required error.
        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidNotAcceptedTypeError: invalid not accepted type error.
        :raises ValidatorFixerMustBeCallable: validator fixer must be callable.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        :raises InvalidRegularExpressionError: invalid regular expression error.
        :raises RegularExpressionMustBeProvidedError: regular expression must be provided error.
        """

        super().__init__(domain, field, **options)

        is_string = isinstance(self.regex, str)
        if not isinstance(self.regex, re.Pattern) and not is_string:
            raise InvalidRegularExpressionError('The provided regular expression for validator '
                                                '[{name}] is invalid. it must be a string '
                                                'containing a regular expression or a Pattern '
                                                'object returned from re.compile() method.'
                                                .format(name=self))

        if is_string and (len(self.regex) <= 0 or self.regex.isspace()):
            raise RegularExpressionMustBeProvidedError('The provided string for regular '
                                                       'expression on validator [{name}] '
                                                       'could not be blank.'
                                                       .format(name=self))

        if is_string:
            flags = options.get('flags')
            if flags is None:
                flags = self.default_flags
            self._pattern = re.compile(self.regex, flags=flags)
        else:
            self._pattern = self.regex

        self._validate_exception_type(self.pattern_not_match_error)

    def _validate_extra(self, value, **options):
        """
        validates the given value.

        this method is intended to be overridden by subclasses.
        it raises an error if validation fails.
        the raised error must be an instance of ValidationError.
        each overridden method must call `super()._validate_extra()`
        preferably at the beginning.

        :param str value: value to be validated.

        :raises ValueDoesNotMatchPatternError: value does not match pattern error.
        """

        super()._validate_extra(value, **options)

        if not self.pattern.match(value):
            raise self.pattern_not_match_error(
                self.pattern_not_match_message.format(param_name=self.localized_name))

    @property
    def pattern(self):
        """
        gets the pattern of this validator.

        :rtype: re.Pattern
        """

        return self._pattern


class EmailValidator(RegexValidator):
    """
    email validator class.
    """

    regex = r'^[a-z0-9]+([a-z0-9\.]*[a-z0-9]+)*[@]\w+[\.]\w{2,3}([\.]\w{2,3})?$'
    pattern_not_match_error = InvalidEmailError
    pattern_not_match_message = _('The provided value for [{param_name}] '
                                  'is not a valid email address.')

    default_minimum_length = 6

    def _validate_extra(self, value, **options):
        """
        validates the given value.

        this method is intended to be overridden by subclasses.
        it raises an error if validation fails.
        the raised error must be an instance of ValidationError.
        each overridden method must call `super()._validate_extra()`
        preferably at the beginning.

        :param str value: value to be validated.

        :raises InvalidEmailError: invalid email error.
        """

        super()._validate_extra(value, **options)

        if '..' in value:
            raise self.pattern_not_match_error(
                self.pattern_not_match_message.format(param_name=self.localized_name))


class IPv4Validator(RegexValidator):
    """
    ipv4 validator class.
    """

    regex = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'

    pattern_not_match_error = InvalidIPv4Error
    pattern_not_match_message = _('The provided value for [{param_name}] '
                                  'is not a valid IPv4 address.')

    default_maximum_length = 15
    default_minimum_length = 7

    def _validate_extra(self, value, **options):
        """
        validates the given value.

        this method is intended to be overridden by subclasses.
        it raises an error if validation fails.
        the raised error must be an instance of ValidationError.
        each overridden method must call `super()._validate_extra()`
        preferably at the beginning.

        :param str value: value to be validated.

        :raises InvalidIPv4Error: invalid ipv4 error.
        """

        super()._validate_extra(value, **options)

        parts = value.split('.')
        for item in parts:
            converted_item = int(item)
            if converted_item < 0 or converted_item > 255:
                raise self.pattern_not_match_error(
                    self.pattern_not_match_message.format(param_name=self.localized_name))


class URLValidator(RegexValidator):
    """
    url validator class.

    this matches urls starting with `www`.
    """

    regex = r'^www\..+\.\w+$'

    pattern_not_match_error = InvalidURLError
    pattern_not_match_message = _('The provided value for [{param_name}] '
                                  'is not a valid url.')

    default_minimum_length = 7

    def _validate_extra(self, value, **options):
        """
        validates the given value.

        this method is intended to be overridden by subclasses.
        it raises an error if validation fails.
        the raised error must be an instance of ValidationError.
        each overridden method must call `super()._validate_extra()`
        preferably at the beginning.

        :param str value: value to be validated.

        :raises InvalidURLError: invalid url error.
        """

        super()._validate_extra(value, **options)

        if ' ' in value or '..' in value:
            raise self.pattern_not_match_error(
                self.pattern_not_match_message.format(param_name=self.localized_name))


class HTTPValidator(URLValidator):
    """
    http validator class.

    this matches urls starting with `http://www`.
    """

    regex = r'^http://www\..+\.\w+$'

    pattern_not_match_error = InvalidHTTPURLError
    pattern_not_match_message = _('The provided value for [{param_name}] '
                                  'is not a valid http url.')

    default_minimum_length = 14


class HTTPSValidator(URLValidator):
    """
    https validator class.

    this matches urls starting with `https://www`.
    """

    regex = r'^https://www\..+\.\w+$'

    pattern_not_match_error = InvalidHTTPSURLError
    pattern_not_match_message = _('The provided value for [{param_name}] '
                                  'is not a valid https url.')

    default_minimum_length = 15

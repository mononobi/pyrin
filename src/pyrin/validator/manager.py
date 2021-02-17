# -*- coding: utf-8 -*-
"""
validator manager module.
"""

from pyrin.core.globals import _
from pyrin.core.structs import Manager, Context, DTO
from pyrin.utils.custom_print import print_warning
from pyrin.validator import ValidatorPackage
from pyrin.validator.interface import AbstractValidatorBase
from pyrin.validator.exceptions import InvalidValidatorTypeError, DuplicatedValidatorError, \
    ValidatorNotFoundError, ValidationError, InvalidEntityForValidationError, \
    InvalidDataForValidationError, ValidatorDomainNotFoundError


class ValidatorManager(Manager):
    """
    validator manager class.
    """

    package_class = ValidatorPackage

    def __init__(self):
        """
        initializes an instance of ValidatorManager.
        """

        super().__init__()

        # a dictionary containing information of registered validators.
        # example: dict(type[BaseEntity] |
        #               str domain: dict(str name: AbstractValidatorBase instance))
        self._validators = Context()

    def register_validator(self, instance, **options):
        """
        registers a new validator or replaces the existing one.

        if `replace=True` is provided. otherwise, it raises an error
        on adding a validator which is already registered.

        :param AbstractValidatorBase instance: validator to be registered.
                                               it must be an instance of
                                               AbstractValidatorBase.

        :keyword bool replace: specifies that if there is another registered
                               validator with the same domain and name, replace
                               it with the new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidValidatorTypeError: invalid validator type error.
        :raises DuplicatedValidatorError: duplicated validator error.
        """

        if not isinstance(instance, AbstractValidatorBase):
            raise InvalidValidatorTypeError('Input parameter [{instance}] is '
                                            'not an instance of [{base}].'
                                            .format(instance=instance,
                                                    base=AbstractValidatorBase))

        domain_validators = self._validators.get(instance.domain)
        if domain_validators is not None:
            old_instance = domain_validators.get(instance.name)
            if old_instance is not None:
                replace = options.get('replace', False)
                if replace is not True:
                    raise DuplicatedValidatorError('There is another registered '
                                                   'validator [{old}] with name '
                                                   '[{name}] for domain [{domain}] '
                                                   'but "replace" option is not set, '
                                                   'so validator [{instance}] '
                                                   'could not be registered.'
                                                   .format(old=old_instance,
                                                           name=instance.name,
                                                           domain=instance.domain,
                                                           instance=instance))

                print_warning('Validator [{old_instance}] is going '
                              'to be replaced by [{new_instance}] '
                              'for domain [{domain}].'
                              .format(old_instance=old_instance,
                                      new_instance=instance,
                                      domain=instance.domain))

        if domain_validators is None:
            domain_validators = DTO()
            self._validators[instance.domain] = domain_validators
        domain_validators[instance.name] = instance
        self._validators[instance.domain] = domain_validators

    def get_domain_validators(self, domain):
        """
        gets all registered validators for given domain.

        it raises an error if domain does not exist.

        :param type[BaseEntity] | str domain: the domain to get its validators.
                                              it could be a type of a BaseEntity
                                              subclass or a string name.

        :raises ValidatorDomainNotFoundError: validator domain not found error.

        :rtype: dict[type[BaseEntity] | str, AbstractValidatorBase]
        """

        if domain not in self._validators:
            raise ValidatorDomainNotFoundError('Validator domain [{name}] does not exist.'
                                               .format(name=domain))

        return self._validators.get(domain)

    def get_validator(self, domain, name):
        """
        gets the registered validator for given domain and name.

        it returns None if no validator found for given name.

        :param type[BaseEntity] | str domain: the domain to get validator from.
                                              it could be a type of a BaseEntity
                                              subclass or a string name.

        :param str name: validator name to get.

        :raises ValidatorDomainNotFoundError: validator domain not found error.

        :rtype: AbstractValidatorBase
        """

        domain_validators = self.get_domain_validators(domain)
        return domain_validators.get(name)

    def validate_field(self, domain, name, value, **options):
        """
        validates the given value with given validator.

        it returns the same value or fixed one.

        :param type[BaseEntity] | str domain: the domain to validate the value for.
                                              it could be a type of a BaseEntity
                                              subclass or a string name.

        :param str name: validator name to be used for validation.
        :param object | list[object] value: value to be validated.

        :keyword bool force: specifies that if there is no validator
                             with specified domain and name, it should
                             raise an error. defaults to False if not provided.

        :keyword bool nullable: determines that provided value could be None.
        :keyword bool is_list: specifies that the value must be a list of items.

        :keyword bool null_items: specifies that list items could be None.
                                  it is only used if `is_list=True` is provided.

        :keyword bool allow_single: specifies that list validator should also
                                    accept single, non list values.
                                    it is only used if `is_list=True` is provided.
                                    defaults to False if not provided.

        :keyword bool allow_empty_list: specifies that list validators should also
                                        accept empty lists.
                                        it is only used if `is_list=True` is provided.
                                        defaults to False if not provided.

        :keyword bool inclusive_minimum: determines that values equal to
                                         accepted minimum should be considered valid.
                                         this argument will only be considered in min
                                         and range validators.

        :keyword bool inclusive_maximum: determines that values equal to
                                         accepted maximum should be considered valid.
                                         this argument will only be considered in max
                                         and range validators.

        :keyword bool allow_blank: determines that empty strings should be
                                   considered valid. this argument will only
                                   be considered in string validators.

        :keyword bool allow_whitespace: determines that whitespace strings should be
                                        considered valid. this argument will only
                                        be considered in string validators.

        :raises ValidatorDomainNotFoundError: validator domain not found error.
        :raises ValidatorNotFoundError: validator not found error.
        :raises ValidationError: validation error.

        :returns: same value or fixed one.
        """

        validator = self.get_validator(domain, name)
        force = options.get('force')
        if force is None:
            force = False

        if force is True and validator is None:
            raise ValidatorNotFoundError('There is no validator with name '
                                         '[{name}] for domain [{domain}].'
                                         .format(name=name, domain=domain))

        if validator is not None:
            return validator.validate(value, **options)

        return value

    def validate_dict(self, domain, data, **options):
        """
        validates available values of given dict.

        it uses the correct validator for each value based on its key name.

        :param type[BaseEntity] | str domain: the domain to validate the values for.
                                              it could be a type of a BaseEntity
                                              subclass or a string name.

        :param dict data: dictionary to validate its values.

        :keyword bool lazy: specifies that all values must be validated first and
                            then a cumulative error must be raised containing a dict
                            of all keys and their corresponding error messages.
                            defaults to True if not provided.

        :keyword bool for_update: specifies that only fields that are present in data
                                  must be validated. even if there are validators for
                                  other fields. it is useful for changing the validation
                                  behavior on insert or update operations. defaults to
                                  False if not provided and all validators will be used.

        :keyword bool nullable: determines that provided values could be None.
        :keyword bool is_list: specifies that the value must be a list of items.

        :keyword bool null_items: specifies that list items could be None.
                                  it is only used if `is_list=True` is provided.

        :keyword bool allow_single: specifies that list validator should also
                                    accept single, non list values.
                                    it is only used if `is_list=True` is provided.
                                    defaults to False if not provided.

        :keyword bool allow_empty_list: specifies that list validators should also
                                        accept empty lists.
                                        it is only used if `is_list=True` is provided.
                                        defaults to False if not provided.

        :keyword bool inclusive_minimum: determines that values equal to
                                         accepted minimum should be considered valid.
                                         this argument will only be considered in min,
                                         max and range validators.

        :keyword bool inclusive_maximum: determines that values equal to
                                         accepted maximum should be considered valid.
                                         this argument will only be considered in min,
                                         max and range validators.

        :keyword bool allow_blank: determines that empty strings should be
                                   considered valid. this argument will only
                                   be considered in string validators.

        :keyword bool allow_whitespace: determines that whitespace strings should be
                                        considered valid. this argument will only
                                        be considered in string validators.

        :keyword BaseEntity entity: an entity instance that the provided data
                                    is the result dict of it.
                                    it will be used to populate fixed values
                                    in the entity.

        :raises InvalidDataForValidationError: invalid data for validation error.
        :raises ValidatorDomainNotFoundError: validator domain not found error.
        :raises ValidatorNotFoundError: validator not found error.
        :raises ValidationError: validation error.
        """

        if data is None:
            raise InvalidDataForValidationError(_('Data for validation could not be None.'))

        cumulative_errors = DTO()
        lazy = options.get('lazy', True)
        for_update = options.get('for_update', False)
        entity = options.get('entity')

        available_data = set(data.keys())
        validator_names = set()
        available_validators = self.get_domain_validators(domain)
        if available_validators is not None:
            validator_names = set(available_validators.keys())

        should_be_validated = validator_names
        if for_update is True:
            should_be_validated = validator_names.intersection(available_data)

        for name in should_be_validated:
            try:
                fixed_value = self.validate_field(domain, name, data.get(name), **options)
                if fixed_value is not None:
                    data[name] = fixed_value
                    if entity is not None:
                        entity.set_attribute(name, fixed_value, silent=True)

            except ValidationError as error:
                if lazy is False:
                    raise error
                else:
                    cumulative_errors[name] = error.description

        if len(cumulative_errors) > 0:
            raise ValidationError(_('Validation failed with some errors.'),
                                  data=cumulative_errors)

    def validate_entity(self, entity, **options):
        """
        validates available values of given entity.

        it uses the correct validator for each value based on its field name.

        :param BaseEntity entity: entity to validate its values.

        :keyword SECURE_TRUE | SECURE_FALSE readable: specifies that any column or attribute
                                                      which has `allow_read=False` or its name
                                                      starts with underscore `_`, should not
                                                      be included in validation. defaults to
                                                      `SECURE_TRUE` if not provided.

        :keyword bool lazy: specifies that all fields must be validated first and
                            then a cumulative error must be raised containing a dict
                            of all field names and their corresponding error messages.
                            defaults to True if not provided.

        :keyword bool for_update: specifies that only fields that are present in data
                                  must be validated. even if there are validators for
                                  other fields. it is useful for changing the validation
                                  behavior on insert or update operations. defaults to
                                  False if not provided and all validators will be used.

        :keyword bool nullable: determines that provided values could be None.
        :keyword bool is_list: specifies that the value must be a list of items.

        :keyword bool null_items: specifies that list items could be None.
                                  it is only used if `is_list=True` is provided.

        :keyword bool allow_single: specifies that list validator should also
                                    accept single, non list values.
                                    it is only used if `is_list=True` is provided.
                                    defaults to False if not provided.

        :keyword bool allow_empty_list: specifies that list validators should also
                                        accept empty lists.
                                        it is only used if `is_list=True` is provided.
                                        defaults to False if not provided.

        :keyword bool inclusive_minimum: determines that values equal to
                                         accepted minimum should be considered valid.
                                         this argument will only be considered in min,
                                         max and range validators.

        :keyword bool inclusive_maximum: determines that values equal to
                                         accepted maximum should be considered valid.
                                         this argument will only be considered in min,
                                         max and range validators.

        :keyword bool allow_blank: determines that empty strings should be
                                   considered valid. this argument will only
                                   be considered in string validators.

        :keyword bool allow_whitespace: determines that whitespace strings should be
                                        considered valid. this argument will only
                                        be considered in string validators.

        :raises InvalidEntityForValidationError: invalid entity for validation error.
        :raises ValidatorDomainNotFoundError: validator domain not found error.
        :raises ValidatorNotFoundError: validator not found error.
        :raises ValidationError: validation error.
        """

        if entity is None:
            raise InvalidEntityForValidationError(_('Entity for validation could not be None.'))

        options.update(entity=entity)
        self.validate_dict(type(entity), entity.to_dict(**options), **options)

    def is_valid_field(self, domain, name, value, **options):
        """
        gets a value indicating that given field is valid.

        :param type[BaseEntity] | str domain: the domain to validate the value for.
                                              it could be a type of a BaseEntity
                                              subclass or a string name.

        :param str name: validator name to be used for validation.
        :param object | list[object] value: value to be validated.

        :keyword bool force: specifies that if there is no validator
                             with specified domain and name, it should
                             raise an error. defaults to False if not provided.

        :keyword bool nullable: determines that provided value could be None.
        :keyword bool is_list: specifies that the value must be a list of items.

        :keyword bool null_items: specifies that list items could be None.
                                  it is only used if `is_list=True` is provided.

        :keyword bool allow_single: specifies that list validator should also
                                    accept single, non list values.
                                    it is only used if `is_list=True` is provided.
                                    defaults to False if not provided.

        :keyword bool allow_empty_list: specifies that list validators should also
                                        accept empty lists.
                                        it is only used if `is_list=True` is provided.
                                        defaults to False if not provided.

        :keyword bool inclusive_minimum: determines that values equal to
                                         accepted minimum should be considered valid.
                                         this argument will only be considered in min
                                         and range validators.

        :keyword bool inclusive_maximum: determines that values equal to
                                         accepted maximum should be considered valid.
                                         this argument will only be considered in max
                                         and range validators.

        :keyword bool allow_blank: determines that empty strings should be
                                   considered valid. this argument will only
                                   be considered in string validators.

        :keyword bool allow_whitespace: determines that whitespace strings should be
                                        considered valid. this argument will only
                                        be considered in string validators.

        :raises ValidatorDomainNotFoundError: validator domain not found error.
        :raises ValidatorNotFoundError: validator not found error.

        :rtype: bool
        """

        try:
            fixed_value = self.validate_field(domain, name, value, **options)
            return value == fixed_value
        except ValidationError:
            return False

    def is_valid_dict(self, domain, data, **options):
        """
        gets a value indicating that given dict has valid values.

        it uses the correct validator for each value based on its key name.

        :param type[BaseEntity] | str domain: the domain to validate the values for.
                                              it could be a type of a BaseEntity
                                              subclass or a string name.

        :param dict data: dictionary to validate its values.

        :keyword bool for_update: specifies that only fields that are present in data
                                  must be validated. even if there are validators for
                                  other fields. it is useful for changing the validation
                                  behavior on insert or update operations. defaults to
                                  False if not provided and all validators will be used.

        :keyword bool nullable: determines that provided values could be None.
        :keyword bool is_list: specifies that the value must be a list of items.

        :keyword bool null_items: specifies that list items could be None.
                                  it is only used if `is_list=True` is provided.

        :keyword bool allow_single: specifies that list validator should also
                                    accept single, non list values.
                                    it is only used if `is_list=True` is provided.
                                    defaults to False if not provided.

        :keyword bool allow_empty_list: specifies that list validators should also
                                        accept empty lists.
                                        it is only used if `is_list=True` is provided.
                                        defaults to False if not provided.

        :keyword bool inclusive_minimum: determines that values equal to
                                         accepted minimum should be considered valid.
                                         this argument will only be considered in min,
                                         max and range validators.

        :keyword bool inclusive_maximum: determines that values equal to
                                         accepted maximum should be considered valid.
                                         this argument will only be considered in min,
                                         max and range validators.

        :keyword bool allow_blank: determines that empty strings should be
                                   considered valid. this argument will only
                                   be considered in string validators.

        :keyword bool allow_whitespace: determines that whitespace strings should be
                                        considered valid. this argument will only
                                        be considered in string validators.

        :raises InvalidDataForValidationError: invalid data for validation error.
        :raises ValidatorDomainNotFoundError: validator domain not found error.
        :raises ValidatorNotFoundError: validator not found error.

        :rtype: bool
        """

        try:
            options.update(lazy=False)
            self.validate_dict(domain, data, **options)
            return True
        except ValidationError:
            return False

    def is_valid_entity(self, entity, **options):
        """
        gets a value indicating that given entity has valid values.

        it uses the correct validator for each value based on its field name.

        :param BaseEntity entity: entity to validate its values.

        :keyword SECURE_TRUE | SECURE_FALSE readable: specifies that any column or attribute
                                                      which has `allow_read=False` or its name
                                                      starts with underscore `_`, should not
                                                      be included in validation. defaults to
                                                      `SECURE_TRUE` if not provided.

        :keyword bool for_update: specifies that only fields that are present in data
                                  must be validated. even if there are validators for
                                  other fields. it is useful for changing the validation
                                  behavior on insert or update operations. defaults to
                                  False if not provided and all validators will be used.

        :keyword bool nullable: determines that provided values could be None.
        :keyword bool is_list: specifies that the value must be a list of items.

        :keyword bool null_items: specifies that list items could be None.
                                  it is only used if `is_list=True` is provided.

        :keyword bool allow_single: specifies that list validator should also
                                    accept single, non list values.
                                    it is only used if `is_list=True` is provided.
                                    defaults to False if not provided.

        :keyword bool allow_empty_list: specifies that list validators should also
                                        accept empty lists.
                                        it is only used if `is_list=True` is provided.
                                        defaults to False if not provided.

        :keyword bool inclusive_minimum: determines that values equal to
                                         accepted minimum should be considered valid.
                                         this argument will only be considered in min,
                                         max and range validators.

        :keyword bool inclusive_maximum: determines that values equal to
                                         accepted maximum should be considered valid.
                                         this argument will only be considered in min,
                                         max and range validators.

        :keyword bool allow_blank: determines that empty strings should be
                                   considered valid. this argument will only
                                   be considered in string validators.

        :keyword bool allow_whitespace: determines that whitespace strings should be
                                        considered valid. this argument will only
                                        be considered in string validators.

        :raises InvalidEntityForValidationError: invalid entity for validation error.
        :raises ValidatorDomainNotFoundError: validator domain not found error.
        :raises ValidatorNotFoundError: validator not found error.

        :rtype: bool
        """

        try:
            options.update(lazy=False)
            self.validate_entity(entity, **options)
            return True
        except ValidationError:
            return False

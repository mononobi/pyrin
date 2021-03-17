# -*- coding: utf-8 -*-
"""
validator services module.
"""

from pyrin.application.services import get_component
from pyrin.validator import ValidatorPackage


def register_validator(instance, **options):
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

    :keyword bool for_find: specifies that this validator must be used
                            on validation for find.
                            defaults to `for_find` attribute of given
                            instance if not provided.

    :raises InvalidValidatorTypeError: invalid validator type error.
    :raises DuplicatedValidatorError: duplicated validator error.
    """

    get_component(ValidatorPackage.COMPONENT_NAME).register_validator(instance, **options)


def get_domain_validators(domain, **options):
    """
    gets all registered validators for given domain.

    it raises an error if domain does not exist.

    :param type[BaseEntity] | str domain: the domain to get its validators.
                                          it could be a type of a BaseEntity
                                          subclass or a string name.

    :keyword bool for_find: specifies that for find validators must be returned.
                            defaults to False if not provided and main validators
                            that have `for_find=False` will be returned.

    :raises ValidatorDomainNotFoundError: validator domain not found error.

    :rtype: dict[type[BaseEntity] | str, AbstractValidatorBase]
    """

    return get_component(ValidatorPackage.COMPONENT_NAME).get_domain_validators(domain,
                                                                                **options)


def get_validator(domain, name, **options):
    """
    gets the registered validator for given domain and name.

    it returns None if no validator found for given name.

    :param type[BaseEntity] | str domain: the domain to get validator from.
                                          it could be a type of a BaseEntity
                                          subclass or a string name.

    :param str name: validator name to get.

    :keyword bool for_find: specifies that for find validator must be returned.
                            defaults to False if not provided and main validator
                            that have `for_find=False` will be returned.

    :raises ValidatorDomainNotFoundError: validator domain not found error.

    :rtype: AbstractValidatorBase
    """

    return get_component(ValidatorPackage.COMPONENT_NAME).get_validator(domain, name, **options)


def try_get_validator(domain, name, **options):
    """
    gets the registered validator for given domain and name.

    it returns None if no validator found for given name or if domain does not exist.

    :param type[BaseEntity] | str domain: the domain to get validator from.
                                          it could be a type of a BaseEntity
                                          subclass or a string name.

    :param str name: validator name to get.

    :keyword bool for_find: specifies that for find validator must be returned.
                            defaults to False if not provided and main validator
                            that have `for_find=False` will be returned.

    :rtype: AbstractValidatorBase
    """

    return get_component(ValidatorPackage.COMPONENT_NAME).try_get_validator(domain, name,
                                                                            **options)


def validate_field(domain, name, value, **options):
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

    :keyword bool for_update: specifies that this field is being
                              validated for update operation.
                              defaults to False if not provided.

    :keyword bool for_find: specifies that this field is being
                            validated for find operation.
                            defaults to False if not provided and only
                            validators that have `for_find=False` will be used.

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

    :raises ValidatorDomainNotFoundError: validator domain not found error.
    :raises ValidatorNotFoundError: validator not found error.
    :raises ValidationError: validation error.

    :returns: same value or fixed one.
    """

    return get_component(ValidatorPackage.COMPONENT_NAME).validate_field(domain, name,
                                                                         value, **options)


def validate_dict(domain, data, **options):
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

    :keyword bool for_find: specifies that this field is being
                            validated for find operation.
                            defaults to False if not provided and only
                            validators that have `for_find=False` will be used.

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

    return get_component(ValidatorPackage.COMPONENT_NAME).validate_dict(domain, data,
                                                                        **options)


def validate_entity(entity, **options):
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

    return get_component(ValidatorPackage.COMPONENT_NAME).validate_entity(entity, **options)


def is_valid_field(domain, name, value, **options):
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

    :keyword bool for_update: specifies that this field is being
                              validated for update operation.
                              defaults to False if not provided.

    :keyword bool for_find: specifies that this field is being
                            validated for find operation.
                            defaults to False if not provided and only
                            validators that have `for_find=False` will be used.

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

    return get_component(ValidatorPackage.COMPONENT_NAME).is_valid_field(domain, name,
                                                                         value, **options)


def is_valid_dict(domain, data, **options):
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

    :keyword bool for_find: specifies that this field is being
                            validated for find operation.
                            defaults to False if not provided and only
                            validators that have `for_find=False` will be used.

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

    return get_component(ValidatorPackage.COMPONENT_NAME).is_valid_dict(domain, data,
                                                                        **options)


def is_valid_entity(entity, **options):
    """
    gets a value indicating that given entity has valid values.

    it uses the correct validator for each value based on its field name.

    :param BaseEntity entity: entity to validate its values.

    :keyword SECURE_TRUE | SECURE_FALSE readable: specifies that any column or attribute
                                                  which has `allow_read=False` or its name
                                                  starts with underscore `_`, should not
                                                  be included in validation. defaults to
                                                  `SECURE_TRUE` if not provided.

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

    return get_component(ValidatorPackage.COMPONENT_NAME).is_valid_entity(entity, **options)


def validate_for_find(domain, data, **options):
    """
    validates available values of given dict for find operation.

    it uses the correct validator for each value based on its key name.
    note that the validation only assures that type of values are correct
    if they are provided. so None values will be accepted too.

    after validation is done, all inputs that are not valid will be removed from
    input data to prevent errors on server. but if you want you can change it
    to raise validation error.

    :param type[BaseEntity] | str domain: the domain to validate the values for.
                                          it could be a type of a BaseEntity
                                          subclass or a string name.

    :param dict data: dictionary to validate its values.

    :keyword bool ignore_errors: specifies that each input that is not valid
                                 must be ignored and removed from inputs.
                                 otherwise it raises validation error.
                                 defaults to False if not provided.

    :raises InvalidDataForValidationError: invalid data for validation error.
    :raises ValidatorDomainNotFoundError: validator domain not found error.
    :raises ValidatorNotFoundError: validator not found error.
    :raises ValidationError: validation error.
    """

    return get_component(ValidatorPackage.COMPONENT_NAME).validate_for_find(domain, data,
                                                                            **options)

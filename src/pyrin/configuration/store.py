# -*- coding: utf-8 -*-
"""
configuration store module.
"""

import os

from copy import deepcopy

import pyrin.converters.deserializer.services as deserializer_services
import pyrin.utils.configuration as config_utils

from pyrin.utils.exceptions import ConfigurationFileNotFoundError as UtilsFileNotFoundError
from pyrin.core.structs import CoreObject, DTO
from pyrin.utils.dictionary import change_key_case
from pyrin.configuration.exceptions import ConfigurationFileNotFoundError, \
    ConfigurationStoreKeyNotFoundError, ConfigurationStoreSectionNotFoundError, \
    ConfigurationStoreDuplicateKeyError, ConfigurationEnvironmentVariableNotFoundError, \
    InvalidConfigurationEnvironmentVariableValueError, \
    ConfigurationStoreAttributeNotFoundException, InvalidEnvironmentVariableKeyError, \
    InvalidPlaceHolderForEnvironmentVariableError


class ConfigStore(CoreObject):
    """
    config store class.

    all configurations will be stored with lowercase keys.
    """

    ACTIVE_SECTION_NAME = 'active'
    SELECTED_SECTION_NAME = 'selected'

    ENV_SEPARATOR = ':'
    # all values of different keys in a config store which start
    # with this, will be get from environment variables.
    ENV_PLACE_HOLDER = 'from_env' + ENV_SEPARATOR

    def __init__(self, name, config_file_path, **options):
        """
        initializes an instance of ConfigStore.

        :param str name: config store name.
        :param str config_file_path: full path of config file.

        :keyword dict defaults: a dict containing values
                                needed for interpolation.
                                defaults to None if not provided.

        :raises ConfigurationFileNotFoundError: configuration file not found error.
        """

        super().__init__()

        self._configs = DTO()
        self._defaults = options.get('defaults', None)
        self._name = name
        self._config_file_path = config_file_path
        self._load(**options)

    def __str__(self):
        """
        gets the string representation of current store.

        :rtype: str
        """

        return '{base} [{store}]'.format(base=super().__str__(), store=self._name)

    def _load(self, **options):
        """
        loads configurations from config file path.

        :keyword dict defaults: a dict containing values
                                needed for interpolation.
                                defaults to None if not provided.

        :raises ConfigurationFileNotFoundError: configuration file not found error.
        """

        try:
            self._configs = config_utils.load(self._config_file_path,
                                              deserializer_services.deserialize,
                                              **options)

        except UtilsFileNotFoundError as error:
            raise ConfigurationFileNotFoundError(error) from error

        self._sync_with_env(**options)

    def reload(self, **options):
        """
        reloads configuration from it's physical file path.

        :keyword dict defaults: a dict containing values
                                needed for interpolation.
                                defaults to None if not provided.

        :raises ConfigurationFileNotFoundError: configuration file not found error.
        """

        defaults = options.get('defaults', None)
        if defaults is None:
            options.update(defaults=self._defaults)
        else:
            self._defaults = defaults

        self._configs.clear()
        self._load(**options)

    def get(self, section, key, **options):
        """
        gets the value of given key from provided section.

        :param str section: config section name.
        :param str key: config key to get it's value.

        :keyword object default: default value if key not present in config section.
                                 if not provided, error will be raised.

        :raises ConfigurationStoreSectionNotFoundError: configuration store
                                                        section not found error.

        :raises ConfigurationStoreKeyNotFoundError: configuration store
                                                    key not found error.
        """

        section_data = self.get_section(section, **options)
        if key in section_data:
            return section_data[key]

        if 'default' not in options:
            raise ConfigurationStoreKeyNotFoundError('Key [{key}] not found in section '
                                                     '[{section}] from config store [{name}].'
                                                     .format(key=key,
                                                             section=section,
                                                             name=self._name))

        return options.get('default')

    def get_active(self, key, **options):
        """
        gets the value of given key from active section of this config store.

        if this store does not have an active section, it raises an error.

        :param str key: config key to get it's value.

        :keyword object default: default value if key not present in config section.
                                 if not provided, error will be raised.

        :raises ConfigurationStoreSectionNotFoundError: configuration store
                                                        section not found error.

        :raises ConfigurationStoreKeyNotFoundError: configuration store
                                                    key not found error.
        """

        active_section = self.get_active_section_name()
        return self.get(active_section, key, **options)

    def get_section_names(self, **options):
        """
        gets all available section names of config store.

        :rtype: list[str]
        """

        return list(self._configs.keys())

    def get_section(self, section, **options):
        """
        gets all key/values stored in given section.

        :param str section: section name.

        :keyword callable converter: a callable to use as case converter for keys.
                                     it should be a callable with a signature
                                     similar to below example:
                                     case_converter(input_dict).

        :raises ConfigurationStoreSectionNotFoundError: configuration store section
                                                        not found error.

        :rtype: dict
        """

        if section not in self._configs:
            raise ConfigurationStoreSectionNotFoundError('Section [{section}] not found in '
                                                         'config store [{name}].'
                                                         .format(section=section,
                                                                 name=self._name))

        result = deepcopy(self._configs.get(section))
        return self._change_key_case(result, **options)

    def get_section_keys(self, section, **options):
        """
        gets all available keys in given section.

        :param str section: section name.

        :keyword callable converter: a callable to use as case converter for keys.
                                     it should be a callable with a signature
                                     similar to below example:
                                     case_converter(input_dict).

        :raises ConfigurationStoreSectionNotFoundError: configuration store section
                                                        not found error.

        :rtype: list[str]
        """

        return list(self.get_section(section, **options).keys())

    def get_all(self, **options):
        """
        gets all available key/values from different sections of this config store.

        in a flat dict, eliminating the sections.
        note that if there are same key names with different values
        in different sections, it raises an error to prevent overwriting
        values. also note that if this config store contains `active` section,
        then the result of `get_active_section` method would be returned.

        :keyword callable converter: a callable to use as case converter for keys.
                                     it should be a callable with a signature
                                     similar to below example:
                                     case_converter(input_dict).

        :raises ConfigurationStoreDuplicateKeyError: configuration store duplicate key error.

        :rtype: dict
        """

        # trying to get active config if available.
        active_config = None
        try:
            active_config = self.get_active_section(**options)
        except ConfigurationStoreAttributeNotFoundException:
            pass

        if active_config is not None:
            return active_config

        flat_dict = DTO()
        for section_data in self._get_sections(**options):
            if isinstance(section_data, dict):
                for key, value in section_data.items():
                    if key in flat_dict and value != flat_dict.get(key):
                        raise ConfigurationStoreDuplicateKeyError('Key [{key}] is available '
                                                                  'in multiple sections of '
                                                                  'config store [{name}] '
                                                                  'with different values.'
                                                                  .format(key=key,
                                                                          name=self._name))
                    flat_dict[key] = value

        return flat_dict

    def get_file_path(self, **options):
        """
        gets config file path of this config store.

        :rtype: str
        """

        return self._config_file_path

    def _change_key_case(self, value, **options):
        """
        returns a copy of input dict with all it's keys
        and nested keys cases modified using given converter.
        if converter is not provided, it returns the inputted dict.

        :param dict value: dict to change it's keys cases.

        :keyword callable converter: a callable to use as case converter.
                                     it should be a callable with a signature
                                     similar to below example:
                                     case_converter(input_dict).

        :rtype: dict
        """

        converter = options.get('converter', None)
        if converter is not None:
            return change_key_case(value, converter)

        return value

    def get_active_section(self, **options):
        """
        gets the active section available in related config file.

        this method gets the section that it's name is under [active]
        section, for example:

        [active]
        selected: production

        [production]
        id: 123
        name: prod

        [development]
        id: 233
        name: dev

        this will return all key/values available under [production].
        if the config store has not an [active] section, this method
        raises an error.

        :keyword callable converter: a callable to use as case converter.
                                     it should be a callable with a signature
                                     similar to below example:
                                     case_converter(input_dict).

        :raises ConfigurationStoreSectionNotFoundError: configuration store
                                                        section not found error.

        :raises ConfigurationStoreKeyNotFoundError: configuration store
                                                    key not found error.

        :rtype: dict
        """

        active_section = self.get_active_section_name()
        return self.get_section(active_section, **options)

    def _get_sections(self, **options):
        """
        gets a list of dictionaries containing all key/values
        for every section of this config store.

        :keyword callable converter: a callable to use as case converter for keys.
                                     it should be a callable with a signature
                                     similar to below example:
                                     case_converter(input_dict).

        :rtype: list[dict]
        """

        return [self.get_section(section, **options)
                for section in self.get_section_names(**options)]

    def _get_from_env(self, key, **options):
        """
        gets the value of given key from environment variable if available.

        otherwise may raise an exception or ignore it depending on `silent` keyword.

        :param str key: key to get it's value from environment variable.

        :keyword bool silent: indicates that if an environment variable for the
                              given key not found, ignore it and return None, otherwise
                              raise an error. defaults to True if not provided.

        :raises ConfigurationEnvironmentVariableNotFoundError: configuration environment
                                                               variable not found error.

        :raises InvalidConfigurationEnvironmentVariableValueError: invalid configuration
                                                                   environment variable
                                                                   value error.

        :rtype: str
        """

        value = os.environ.get(key)
        silent = options.get('silent', True)
        if value is None and silent is not True:
            raise ConfigurationEnvironmentVariableNotFoundError('Configuration environment '
                                                                'variable [{key}] not found.'
                                                                .format(key=key))

        if value is not None and len(value.strip()) == 0 and silent is not True:
            raise InvalidConfigurationEnvironmentVariableValueError('Configuration environment '
                                                                    'variable [{key}] has '
                                                                    'an invalid value.'
                                                                    .format(key=key))

        return value

    def _sync_with_env(self, **options):
        """
        synchronizes all keys with None value of this config store.

        with environment variables if available. it searches for environment
        variables with name `STORE_SECTION_KEY`. for example `API_GENERAL_NAMESPACE`.
        it also updates all keys that their values start with `ENV_PLACE_HOLDER`
        from environment variables.

        :keyword bool silent: indicates that if an environment variable for the
                              config key not found, ignore it and return None, otherwise
                              raise an error. defaults to True.
                              note that this option is only for keys that have None value.
                              but those keys that have `ENV_PLACE_HOLDER` will always cause
                              an error if environment variable not found for them.

        :raises ConfigurationEnvironmentVariableNotFoundError: configuration environment
                                                               variable not found error.

        :raises InvalidConfigurationEnvironmentVariableValueError: invalid configuration
                                                                   environment variable
                                                                   value error.

        :raises InvalidPlaceHolderForEnvironmentVariableError: invalid place holder for
                                                               environment variable error.

        :raises InvalidEnvironmentVariableKeyError: invalid environment variable key error.
        """

        for section_name in self.get_section_names():
            section = self.get_section(section_name)
            for key, value in section.items():
                if self._should_try_env(value) is True:
                    env_value = None
                    if value is None:
                        key_name = self._get_env_key_name(self._name, section_name, key)
                        env_value = self._get_from_env(key_name, **options)
                    else:
                        env_key = self._extract_env_key(section_name, key, value)
                        env_value = self._get_from_env(env_key, silent=False)
                    converted_value = deserializer_services.deserialize(env_value)
                    self._configs[section_name][key] = converted_value

    def _get_env_key_name(self, store, section, key):
        """
        gets key name for given inputs to get it from environment variables.

        it generates key name in this format: `STORE_SECTION_KEY`.
        for example: `API_GENERAL_NAMESPACE`.

        :param str store: config store name.
        :param str section: config store section name.
        :param str key: section key name.

        :rtype: str
        """

        return '{store}_{section}_{key}'.format(store=store.upper(),
                                                section=section.upper(),
                                                key=key.upper())

    def _extract_env_key(self, section, key, value):
        """
        extracts environment variable key name from given value.

        :param str section: config section name.
        :param str key: key to get it's value from environment variable.
        :param str value: value to get environment variable key name from it.

        :raises InvalidPlaceHolderForEnvironmentVariableError: invalid place holder for
                                                               environment variable error.

        :raises InvalidEnvironmentVariableKeyError: invalid environment variable key error.

        :rtype: str
        """

        if self.ENV_SEPARATOR not in value:
            raise InvalidPlaceHolderForEnvironmentVariableError('Environment variable place '
                                                                'holder must contain a [{sep}] '
                                                                'character. but value [{value}] '
                                                                'for key [{key}] of section '
                                                                '[{section}] in config store '
                                                                '[{store}] does not contain any '
                                                                'of it.'
                                                                .format(sep=self.ENV_SEPARATOR,
                                                                        value=value, key=key,
                                                                        section=section,
                                                                        store=self))
        separator_index = value.index(self.ENV_SEPARATOR)
        env_key = value[separator_index + 1:]
        if env_key in (None, ''):
            raise InvalidEnvironmentVariableKeyError('Provided environment variable name is '
                                                     'invalid for config key [{key}] of section '
                                                     '[{section}] in config store [{store}].'
                                                     .format(key=key, section=section,
                                                             store=self))
        return env_key

    def _should_try_env(self, value):
        """
        gets a value indicating that given key could be get from environment variables.

        if the value is None or it starts with 'ENV_PLACE_HOLDER' this method returns true.

        :param object value: current value of given key in config file.

        :rtype: bool
        """

        return value is None or self._is_env_required(value)

    def _is_env_required(self, value):
        """
        gets a value indicating that given key must be get from environment variables.

        if the value starts with 'ENV_PLACE_HOLDER' this method returns true.

        :param object value: current value of given key in config file.

        :rtype: bool
        """

        return isinstance(value, str) and value.startswith(self.ENV_PLACE_HOLDER)

    def get_active_section_name(self):
        """
        gets the active section name of this config store if available.

        if the store does not have an active section, it raises an error.

        :raises ConfigurationStoreSectionNotFoundError: configuration store
                                                        section not found error.

        :raises ConfigurationStoreKeyNotFoundError: configuration store
                                                    key not found error.

        :rtype: str
        """

        return self.get(self.ACTIVE_SECTION_NAME, self.SELECTED_SECTION_NAME)

    def get_all_sections(self, **options):
        """
        gets all sections and their keys of current config store.

        :raises ConfigurationStoreNotFoundError: configuration store not found error.

        :rtype: dict
        """

        return deepcopy(self._configs)

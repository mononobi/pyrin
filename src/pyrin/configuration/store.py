# -*- coding: utf-8 -*-
"""
configuration store module.
"""

from configparser import ConfigParser

import pyrin.converters.deserializer.services as deserializer_services

from pyrin.core.context import CoreObject, DTO
from pyrin.utils.dictionary import change_key_case
from pyrin.configuration.exceptions import ConfigurationFileNotFoundError, \
    ConfigurationStoreKeyNotFoundError, ConfigurationStoreSectionNotFoundError, \
    ConfigurationStoreDuplicateKeyError


class ConfigStore(CoreObject):
    """
    config store class.
    all configurations will be stored with lowercase keys.
    """

    ACTIVE_SECTION_NAME = 'active'
    SELECTED_SECTION_NAME = 'selected'

    def __init__(self, name, config_file_path, **options):
        """
        initializes a new ConfigStore.

        :param str name: config store name.
        :param str config_file_path: full path of config file.
        """

        CoreObject.__init__(self)

        self._configs = DTO()
        self._name = name
        self._config_file_path = config_file_path
        self._load(**options)

    def _load(self, **options):
        """
        loads configurations from config file path.

        :raises ConfigurationFileNotFoundError: configuration file not found error.
        """

        parser = ConfigParser()
        if len(parser.read(self._config_file_path)) == 0:
            raise ConfigurationFileNotFoundError('Configuration file [{file}] not found.'
                                                 .format(file=self._config_file_path))

        for section in parser.sections():
            values = parser.items(section)
            dic_values = DTO()
            for single_value in values:
                dic_values[single_value[0]] = single_value[1]

            self._configs[section] = deserializer_services.deserialize(dic_values)

    def reload(self, **options):
        """
        reloads configuration from it's physical file path.

        :raises ConfigurationFileNotFoundError: configuration file not found error.
        """

        self._configs.clear()
        self._load(**options)

    def get(self, section, key, **options):
        """
        gets the value of given key from provided section.

        :param str section: config section name.
        :param str key: config key to get it's value.

        :keyword object default_value: default value if key not present in config section.
                                       if not provided, error will be raised.

        :raises ConfigurationStoreSectionNotFoundError: configuration store
                                                        section not found error.

        :raises ConfigurationStoreKeyNotFoundError: configuration store
                                                    key not found error.

        :rtype: object
        """

        section_data = self.get_section(section, **options)
        if key in section_data.keys():
            return section_data[key]

        if 'default_value' not in options.keys():
            raise ConfigurationStoreKeyNotFoundError('Key [{key}] not found in section '
                                                     '[{section}] from config store [{name}].'
                                                     .format(key=key,
                                                             section=section,
                                                             name=self._name))

        return options.get('default_value')

    def get_section_names(self, **options):
        """
        gets all available section names of config store.

        :rtype: list[str]
        """

        return self._configs.keys()

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

        if section not in self._configs.keys():
            raise ConfigurationStoreSectionNotFoundError('Section [{section}] not found in '
                                                         'config store [{name}].'
                                                         .format(section=section,
                                                                 name=self._name))

        result = self._configs.get(section)

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

        return self.get_section(section, **options).keys()

    def get_all(self, **options):
        """
        gets all available key/values from different sections of
        this config store in a flat dict, eliminating the sections.
        note that if there are same key names in different
        sections, it raises an error to prevent overwriting values.
        also note that if this config store contains `active` section,
        then the result of `get_active` method would be returned.

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
            active_config = self.get_active(**options)
        except (ConfigurationStoreSectionNotFoundError,
                ConfigurationStoreKeyNotFoundError):
            pass

        if active_config is not None:
            return active_config

        flat_dict = DTO()
        for section_data in self._get_sections(**options):
            if isinstance(section_data, dict):
                for key, value in section_data.items():
                    if key in flat_dict.keys():
                        raise ConfigurationStoreDuplicateKeyError('Key [{key}] is available '
                                                                  'in multiple sections of '
                                                                  'config store [{name}].'
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

    def get_active(self, **options):
        """
        gets the active configuration available in related file.
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

        selected_name = self.get(self.ACTIVE_SECTION_NAME, self.SELECTED_SECTION_NAME)
        return self.get_section(str(selected_name), **options)

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


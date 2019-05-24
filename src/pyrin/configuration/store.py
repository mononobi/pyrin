# -*- coding: utf-8 -*-
"""
configuration store module.
"""

from configparser import ConfigParser

import pyrin.converters.deserializer.services as deserializer_services
from pyrin.configuration.exceptions import ConfigurationFileNotFoundError, \
    ConfigurationStoreSectionOrKeyNotFoundError, ConfigurationStoreSectionNotFoundError, \
    ConfigurationStoreDuplicateKeyError

from pyrin.context import CoreObject, DTO
from pyrin.utils.dictionary import change_key_case


class ConfigStore(CoreObject):
    """
    config store class.
    all configurations will be stored with lowercase keys.
    """

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

        :raises ConfigurationStoreSectionOrKeyNotFoundError: configuration store section
                                                             or key not found error.

        :rtype: object
        """

        if section in self._configs.keys() and \
           key in self._configs[section].keys():
            return self._configs[section][key]

        if 'default_value' not in options.keys():
            raise ConfigurationStoreSectionOrKeyNotFoundError('Configuration with section '
                                                              '[{section}] and key [{key}] '
                                                              'not found in config '
                                                              'store [{name}].'
                                                              .format(section=section,
                                                                      key=key,
                                                                      name=self._name))

        return options.get('default_value')

    def get_section_names(self):
        """
        gets all available section names of config store.

        :rtype: list[str]
        """

        return self._configs.keys()

    def get_section(self, section, **options):
        """
        gets all key/values stored in given section.

        :param str section: section name.

        :keyword callable converter: a callable to use as keys case converter.

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

        converter = options.get('converter', None)
        if converter is not None:
            return change_key_case(result, converter)

        return result

    def get_section_keys(self, section):
        """
        gets all available keys in given section.

        :param str section: section name.

        :rtype: list[str]
        """

        return self.get_section(section).keys()

    def get_all(self, **options):
        """
        gets all available key/values from different sections of
        this config store in a flat dict, eliminating the sections.
        note that if there are same key names in different
        sections, it raises an error to prevent overwriting values.

        :keyword callable converter: a callable to use as keys case converter.

        :raises ConfigurationStoreDuplicateKeyError: configuration store duplicate key error.

        :rtype: dict
        """

        flat_dict = DTO()
        for section, value in self._configs.items():
            if isinstance(value, dict):
                for key, data in value.items():
                    if key in flat_dict.keys():
                        raise ConfigurationStoreDuplicateKeyError('Key [{key}] is available '
                                                                  'in multiple sections of '
                                                                  'config store [{name}].'
                                                                  .format(key=key,
                                                                          name=self._name))
                    flat_dict[key] = data

        converter = options.get('converter', None)
        if converter is not None:
            return change_key_case(flat_dict, converter)

        return flat_dict

    def get_file_path(self):
        """
        gets config file path of this config store.

        :rtype: str
        """

        return self._config_file_path

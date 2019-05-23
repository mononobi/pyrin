# -*- coding: utf-8 -*-
"""
configuration store module.
"""

from configparser import ConfigParser

import pyrin.converters.deserializer.services as deserializer_services

from pyrin.context import CoreObject
from pyrin.exceptions import CoreFileNotFoundError, CoreKeyError


class ConfigStore(CoreObject):
    """
    config store class.
    """

    def __init__(self, name, config_file_path, **options):
        """
        initializes a new ConfigStoreBase.

        :param str name: config store name.
        :param str config_file_path: full path of config file.
        """

        CoreObject.__init__(self)

        self._configs = {}
        self._name = name
        self._config_file_path = config_file_path
        self._load(**options)

    def _load(self, **options):
        """
        loads configuration from given file and stores it with given name.
        """

        parser = ConfigParser()
        if len(parser.read(self._config_file_path)) == 0:
            raise CoreFileNotFoundError('Configuration file [{file}] not found.'
                                        .format(file=self._config_file_path))

        for section in parser.sections():
            values = parser.items(section)
            dic_values = {}
            for single_value in values:
                dic_values[single_value[0]] = single_value[1]

            self._configs[section] = deserializer_services.deserialize(dic_values)

    def reload(self, **options):
        """
        reloads the configuration from it's file.
        """

        self._configs.clear()
        self._load(**options)

    def get(self, section, key, **options):
        """
        gets the value of given key from provided section.

        :param str section: config section name.
        :param str key: config key to get it's value.

        :keyword object default_value: default value if key not present in config store.
                                       if not provided, error will be raised.

        :raises CoreKeyError: core key error.

        :rtype: object
        """

        if section in self._configs.keys() and \
           key in self._configs[section].keys():
            return self._configs[section][key]

        if 'default_value' not in options.keys():
            raise CoreKeyError('Configuration with section [{section}] and key '
                               '[{key}] not found in config store [{store}].'
                               .format(section=section, key=key, store=self._name))

        return options.get('default_value')

    def get_section_names(self):
        """
        gets all the available section names of config store.

        :rtype: list[str]
        """

        return self._configs.keys()

    def get_section(self, section):
        """
        gets all key/values stored in given section.

        :param str section: section name.

        :raises CoreKeyError: core key error.

        :rtype: dict
        """

        if section not in self._configs.keys():
            raise CoreKeyError('Section [{section}] not found in config store [{store}].'
                               .format(section=section, store=self._name))

        return self._configs.get(section)

    def get_section_keys(self, section):
        """
        gets all available keys in given section.

        :param str section: section name.

        :rtype: list[str]
        """

        return self.get_section(section).keys()

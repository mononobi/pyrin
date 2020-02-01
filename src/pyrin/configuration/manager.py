# -*- coding: utf-8 -*-
"""
configuration manager module.
"""

import os

import pyrin.application.services as application_services

from pyrin.configuration.store import ConfigStore
from pyrin.core.context import Context, Manager
from pyrin.configuration.exceptions import ConfigurationStoreExistedError, \
    ConfigurationSettingsPathNotExistedError, ConfigurationStoreNotFoundError, \
    ConfigurationFileNotFoundError
from pyrin.utils.custom_print import print_warning


class ConfigurationManager(Manager):
    """
    configuration manager class.
    """

    def __init__(self, **options):
        """
        initializes an instance of ConfigurationManager.
        """

        super().__init__()

        self._config_stores = Context()
        self._settings_path = application_services.get_settings_path()

    def _add_config_store(self, name, file_path, **options):
        """
        adds a new config store for given file with the specified name.

        :param str name: config store name.
        :param str file_path: config file full path.

        :keyword bool ignore_on_existed: specifies that it should not raise an
                                         error if a config store with given name
                                         has been already loaded.
                                         defaults to False if not provided.

        :raises ConfigurationStoreExistedError: configuration store existed error.
        """

        ignore = options.get('ignore_on_existed', False)
        if name in self._config_stores:
            if ignore is not True:
                raise ConfigurationStoreExistedError('Config store with name [{name}] already '
                                                     'existed, config file names must be unique.'
                                                     .format(name=name))
            else:
                print_warning('Config store with name [{name}] already '
                              'existed, it will be ignored.'
                              .format(name=name))
                return

        self._config_stores[name] = ConfigStore(name, file_path, **options)

    def _is_config_file(self, file_name):
        """
        gets a value indicating that given file name belongs to a config file.

        :param str file_name: file name.

        :rtype: bool
        """

        return file_name.endswith('.config')

    def load_configuration(self, name, **options):
        """
        loads the given configuration if relevant file is
        available in settings path.

        :param str name: configuration name.

        :keyword bool silent: specifies that if a related configuration file
                              for the given name not found, ignore it.
                              otherwise raise an error. defaults to False.

        :keyword bool ignore_on_existed: specifies that it should not raise an
                                         error if a config store with given name
                                         has been already loaded.
                                         defaults to False if not provided.

        :raises ConfigurationSettingsPathNotExistedError: configuration settings
                                                          path not existed error.

        :raises ConfigurationFileNotFoundError: configuration file not found error.
        :raises ConfigurationStoreExistedError: configuration store existed error.
        """

        file_path = self._get_relevant_file_path(name, **options)
        if file_path is not None:
            self._add_config_store(name, file_path, **options)

    def load_configurations(self, *names, **options):
        """
        loads the given configurations if relevant files is
        available in settings path.

        :param str names: configuration names as arguments.

        :keyword bool silent: specifies that if a related configuration file
                              for any of the given names not found, ignore it.
                              otherwise raise an error. defaults to False.

        :keyword bool ignore_on_existed: specifies that it should not raise an
                                         error if a config store with given name
                                         has been already loaded.
                                         defaults to False if not provided.

        :raises ConfigurationSettingsPathNotExistedError: configuration settings
                                                          path not existed error.

        :raises ConfigurationFileNotFoundError: configuration file not found error.
        :raises ConfigurationStoreExistedError: configuration store existed error.
        """

        for single_name in names:
            self.load_configuration(single_name, **options)

    def _get_relevant_file_path(self, name, **options):
        """
        gets the relevant file path to specified config name in settings folder.

        :param str name: config store name.

        :keyword bool silent: specifies that if a related configuration file
                              for the given store name not found, ignore it.
                              otherwise raise an error. defaults to False.

        :raises ConfigurationSettingsPathNotExistedError: configuration settings
                                                          path not existed error.

        :raises ConfigurationFileNotFoundError: configuration file not found error.
        """

        if not os.path.isdir(self._settings_path):
            raise ConfigurationSettingsPathNotExistedError('Settings path [{path}] '
                                                           'does not exist.'
                                                           .format(path=self._settings_path))

        files = os.listdir(self._settings_path)

        for single_file in files:
            single_file_name = os.path.splitext(single_file)[0]
            if single_file_name == name and \
               self._is_config_file(single_file):
                return os.path.join(self._settings_path, single_file)

        silent = options.get('silent', False)
        if silent is not True:
            raise ConfigurationFileNotFoundError('Config name [{name}] does not '
                                                 'have any related configuration '
                                                 'file in [{settings}].'
                                                 .format(name=name,
                                                         settings=self._settings_path))
        return None

    def reload(self, store_name, **options):
        """
        reloads the configuration store from it's relevant file.

        :param str store_name: config store name to be reloaded.

        :raises ConfigurationStoreNotFoundError: configuration store not found error.
        """

        self._get_config_store(store_name).reload(**options)

    def get_file_path(self, store_name, **options):
        """
        gets the configuration file path for given config store.

        :param str store_name: config store name to get it's file path.

        :raises ConfigurationStoreNotFoundError: configuration store not found error.
        """

        if store_name in self._config_stores.keys():
            return self._get_config_store(store_name).get_file_path(**options)

        return self._get_relevant_file_path(store_name, **options)

    def get(self, store_name, section, key, **options):
        """
        gets the value of specified key from provided section of given config store.

        :param str store_name: config store name.
        :param str section: config section name.
        :param str key: config key to get it's value.

        :keyword object default_value: default value if key not present in config section.
                                       if not provided, error will be raised.

        :raises ConfigurationStoreNotFoundError: configuration store not found error.

        :raises ConfigurationStoreSectionNotFoundError: configuration store
                                                        section not found error.

        :raises ConfigurationStoreKeyNotFoundError: configuration store
                                                    key not found error.
        """

        return self._get_config_store(store_name).get(section, key, **options)

    def get_active(self, store_name, key, **options):
        """
        gets the value of given key from active section of given config store.
        if this store does not have an active section, it raises an error.

        :param str store_name: config store name.
        :param str key: config key to get it's value.

        :keyword object default_value: default value if key not present in config section.
                                       if not provided, error will be raised.

        :raises ConfigurationStoreNotFoundError: configuration store not found error.

        :raises ConfigurationStoreSectionNotFoundError: configuration store
                                                        section not found error.

        :raises ConfigurationStoreKeyNotFoundError: configuration store
                                                    key not found error.
        """

        return self._get_config_store(store_name).get_active(key, **options)

    def get_section_names(self, store_name, **options):
        """
        gets all available section names of given config store.

        :param str store_name: config store name.

        :raises ConfigurationStoreNotFoundError: configuration store not found error.

        :rtype: list[str]
        """

        return self._get_config_store(store_name).get_section_names(**options)

    def get_section(self, store_name, section, **options):
        """
        gets all key/values stored in given section of specified config store.

        :param str store_name: config store name.
        :param str section: section name.

        :keyword callable converter: a callable to use as case converter for keys.
                                     it should be a callable with a signature
                                     similar to below example:
                                     case_converter(input_dict).

        :raises ConfigurationStoreNotFoundError: configuration store not found error.

        :raises ConfigurationStoreSectionNotFoundError: configuration store section
                                                        not found error.

        :rtype: dict
        """

        return self._get_config_store(store_name).get_section(section, **options)

    def get_section_keys(self, store_name, section, **options):
        """
        gets all available keys in given section of specified config store.

        :param str store_name: config store name.
        :param str section: section name.

        :keyword callable converter: a callable to use as case converter for keys.
                                     it should be a callable with a signature
                                     similar to below example:
                                     case_converter(input_dict).

        :raises ConfigurationStoreNotFoundError: configuration store not found error.

        :raises ConfigurationStoreSectionNotFoundError: configuration store section
                                                        not found error.

        :rtype: list[str]
        """

        return self._get_config_store(store_name).get_section_keys(section, **options)

    def get_all(self, store_name, **options):
        """
        gets all available key/values from different sections of
        given config store in a flat dict, eliminating the sections.
        note that if there are same key names in different
        sections, it raises an error to prevent overwriting values.
        also note that if the config store contains `active` section,
        then the result of `get_active_section` method would be returned.

        :param str store_name: config store name.

        :keyword callable converter: a callable to use as case converter for keys.
                                     it should be a callable with a signature
                                     similar to below example:
                                     case_converter(input_dict).

        :raises ConfigurationStoreNotFoundError: configuration store not found error.
        :raises ConfigurationStoreDuplicateKeyError: configuration store duplicate key error.

        :rtype: dict
        """

        return self._get_config_store(store_name).get_all(**options)

    def get_active_section(self, store_name, **options):
        """
        gets the active section available in given config store.
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

        :param str store_name: config store name.

        :keyword callable converter: a callable to use as case converter.
                                     it should be a callable with a signature
                                     similar to below example:
                                     case_converter(input_dict).

        :raises ConfigurationStoreNotFoundError: configuration store not found error.

        :raises ConfigurationStoreSectionNotFoundError: configuration store section
                                                        not found error.

        :raises ConfigurationStoreKeyNotFoundError: configuration store
                                                    key not found error.

        :rtype: dict
        """

        return self._get_config_store(store_name).get_active_section(**options)

    def _get_config_store(self, name):
        """
        gets the specified config store.

        :param str name: config store name.

        :raises ConfigurationStoreNotFoundError: configuration store not found error.

        :rtype: ConfigStore
        """

        if name not in self._config_stores.keys():
            raise ConfigurationStoreNotFoundError('Config store [{name}] not found.'
                                                  .format(name=name))

        return self._config_stores[name]

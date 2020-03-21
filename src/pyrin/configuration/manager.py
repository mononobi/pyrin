# -*- coding: utf-8 -*-
"""
configuration manager module.
"""

import os

import pyrin.application.services as application_services
import pyrin.utils.path as path_utils

from pyrin.configuration.store import ConfigStore
from pyrin.core.structs import Context, Manager
from pyrin.configuration.exceptions import ConfigurationStoreExistedError, \
    ConfigurationStoreNotFoundError, ConfigurationFileNotFoundError, ConfigurationFileExistedError


class ConfigurationManager(Manager):
    """
    configuration manager class.
    """

    # config extension to be used for config file names.
    CONFIG_EXTENSION = '.config'

    def __init__(self, **options):
        """
        initializes an instance of ConfigurationManager.
        """

        super().__init__()

        self._config_stores = Context()
        self._settings_path = application_services.get_settings_path()
        self._default_settings_path = application_services.get_default_settings_path()

    def _add_config_store(self, name, file_path, **options):
        """
        adds a new config store for given file with the specified name.

        :param str name: config store name.
        :param str file_path: config file full path.

        :keyword dict defaults: a dict containing values
                                needed for interpolation.
                                defaults to None if not provided.

        :keyword bool ignore_on_existed: specifies that it should not raise an
                                         error if a config store with given name
                                         has been already loaded.
                                         defaults to False if not provided.

        :raises ConfigurationStoreExistedError: configuration store existed error.
        """

        ignore = options.get('ignore_on_existed', False)
        if name in self._config_stores:
            if ignore is not True:
                raise ConfigurationStoreExistedError('Config store name [{name}] already '
                                                     'existed, config store names must be unique.'
                                                     .format(name=name))
        else:
            self._config_stores[name] = ConfigStore(name, file_path, **options)

    def _is_config_file(self, file_name):
        """
        gets a value indicating that given file name belongs to a config file.

        :param str file_name: file name.

        :rtype: bool
        """

        return file_name.endswith(self.CONFIG_EXTENSION)

    def load_configuration(self, name, **options):
        """
        loads the given configuration if relevant file is available in settings path.

        it creates the config file in application settings path if
        config file is only available in pyrin default settings.

        :param str name: configuration name.

        :keyword dict defaults: a dict containing values
                                needed for interpolation.
                                defaults to None if not provided.

        :keyword bool silent: specifies that if a related configuration file
                              for the given name not found, ignore it.
                              otherwise raise an error. defaults to False.

        :keyword bool ignore_on_existed: specifies that it should not raise an
                                         error if a config store with given name
                                         has been already loaded.
                                         defaults to False if not provided.

        :raises ConfigurationFileNotFoundError: configuration file not found error.
        :raises ConfigurationStoreExistedError: configuration store existed error.
        """

        file_path = self._get_relevant_file_path(name, **options)
        if file_path is not None:
            self._add_config_store(name, file_path, **options)
            self.create_config_file(name, ignore_on_existed=True)

    def load_configurations(self, *names, **options):
        """
        loads the given configurations if relevant files is available in settings path.

        it creates the config files in application settings path if
        config files are only available in pyrin default settings.

        :param str names: configuration names as arguments.

        :keyword dict defaults: a dict containing values
                                needed for interpolation.
                                defaults to None if not provided.

        :keyword bool silent: specifies that if a related configuration file
                              for any of the given names not found, ignore it.
                              otherwise raise an error. defaults to False.

        :keyword bool ignore_on_existed: specifies that it should not raise an
                                         error if a config store with given name
                                         has been already loaded.
                                         defaults to False if not provided.

        :raises ConfigurationFileNotFoundError: configuration file not found error.
        :raises ConfigurationStoreExistedError: configuration store existed error.
        """

        for single_name in names:
            self.load_configuration(single_name, **options)

    def _get_relevant_file_path(self, name, **options):
        """
        gets the relevant file path to specified store name in settings folder.
        it returns None if the file is not available and `silent=True` is given.

        :param str name: config store name.

        :keyword bool silent: specifies that if a related configuration file
                              for the given store name not found, ignore it.
                              otherwise raise an error. defaults to False.

        :raises ConfigurationFileNotFoundError: configuration file not found error.
        """

        config_name = self._get_file_name(name)
        config_path = path_utils.get_first_available_file(self._settings_path,
                                                          self._default_settings_path,
                                                          file_name=config_name)

        silent = options.get('silent', False)
        if config_path is None and silent is not True:
            raise ConfigurationFileNotFoundError('Config store name [{name}] does not '
                                                 'have any related configuration '
                                                 'file in application settings.'
                                                 .format(name=name))
        return config_path

    def _get_file_name(self, store):
        """
        gets the generic file name for given store name.

        note that the purpose of this method is different from `get_file_name()`
        method, this method makes a generic file name without any assertion
        for the file to be really existed. if you want to assert the existence
        of the file, you should use `get_file_name()` method.

        :param str store: store name to make file name for it.

        :rtype: str
        """

        return '{store}{extension}'.format(store=store, extension=self.CONFIG_EXTENSION)

    def reload(self, store_name, **options):
        """
        reloads the configuration store from it's relevant file.

        :param str store_name: config store name to be reloaded.

        :keyword dict defaults: a dict containing values
                                needed for interpolation.
                                defaults to None if not provided.

        :raises ConfigurationStoreNotFoundError: configuration store not found error.
        """

        self._get_config_store(store_name).reload(**options)

    def get_file_path(self, store_name, **options):
        """
        gets the configuration file path for given config store.

        :param str store_name: config store name to get its file path.

        :keyword bool silent: specifies that if a related configuration file
                              for the given store name not found, ignore it.
                              otherwise raise an error. defaults to False.

        :raises ConfigurationFileNotFoundError: configuration file not found error.
        """

        if store_name in self._config_stores.keys():
            return self._get_config_store(store_name).get_file_path(**options)

        return self._get_relevant_file_path(store_name, **options)

    def get_file_name(self, store_name, **options):
        """
        gets the configuration file name for given config store.

        for example: `database.config`

        :param str store_name: config store name to get its file name.

        :keyword bool silent: specifies that if a related configuration file
                              for the given store name not found, ignore it.
                              otherwise raise an error. defaults to False.

        :raises ConfigurationFileNotFoundError: configuration file not found error.
        """

        file_path = self.get_file_path(store_name, **options)
        if file_path is not None:
            return os.path.basename(file_path)

        return None

    def create_config_files(self, *stores, **options):
        """
        creates the config files for given store names in application settings path.

        it creates files based on files available in pyrin default settings.

        :param str stores: store names to create config files for them.

        :keyword bool ignore_on_existed: specifies that if a config file for a
                                         store name is already existed, ignore
                                         it, otherwise raise an error.
                                         defaults to False if not provided.

        :raises ConfigurationFileNotFoundError: configuration file not found error.
        :raises ConfigurationFileExistedError: configuration file existed error.
        """

        for store_name in stores:
            self.create_config_file(store_name, **options)

    def create_config_file(self, store, **options):
        """
        creates the config file for given store name in application settings path.

        it creates the file based on file available in pyrin default settings.

        :param str store: store name to create config file for it.

        :keyword bool ignore_on_existed: specifies that if a config file for the
                                         store name is already existed, ignore
                                         it, otherwise raise an error.
                                         defaults to False if not provided.

        :raises ConfigurationFileNotFoundError: configuration file not found error.
        :raises ConfigurationFileExistedError: configuration file existed error.
        """

        source_path = self.get_file_path(store)
        config_name = self._get_file_name(store)
        config_path = os.path.abspath(os.path.join(self._settings_path, config_name))
        ignore_on_existed = options.get('ignore_on_existed', False)

        if os.path.exists(config_path):
            if ignore_on_existed is False:
                raise ConfigurationFileExistedError('Configuration file for store [{store}] '
                                                    'is already existed at [{file_path}].'
                                                    .format(store=store, file_path=config_path))
        else:
            if os.path.exists(self._settings_path) is False:
                path_utils.create_directory(self._settings_path)

            path_utils.copy_file(source_path, config_path)

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
        note that if there are same key names with different values
        in different sections, it raises an error to prevent overwriting
        values. also note that if given config store contains `active` section,
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

    def get_active_section_name(self, store_name):
        """
        gets the active section name of given config store if available.
        if the store does not have an active section, it raises an error.

        :param str store_name: config store name.

        :raises ConfigurationStoreNotFoundError: configuration store not found error.

        :raises ConfigurationStoreSectionNotFoundError: configuration store
                                                        section not found error.

        :raises ConfigurationStoreKeyNotFoundError: configuration store
                                                    key not found error.

        :rtype: str
        """

        return self._get_config_store(store_name).get_active_section_name()

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

    def get_all_sections(self, store_name, **options):
        """
        gets all sections and their keys of given config store.

        :param str store_name: config store name.

        :raises ConfigurationStoreNotFoundError: configuration store not found error.

        :rtype: dict
        """

        return self._get_config_store(store_name).get_all_sections(**options)

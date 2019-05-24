# -*- coding: utf-8 -*-
"""
configuration manager module.
"""

import os

import pyrin.application.services as application_services

from pyrin.configuration.store import ConfigStore
from pyrin.context import CoreObject
from pyrin.exceptions import CoreNotADirectoryError, CoreKeyError, CoreFileNotFoundError


class ConfigurationStoreNotFoundError(CoreKeyError):
    """
    configuration store not found error.
    """


class ConfigurationStoreExistedError(CoreKeyError):
    """
    configuration store existed error.
    """


class ConfigurationSettingsPathNotExistedError(CoreNotADirectoryError):
    """
    configuration settings path not existed error.
    """


class ConfigurationRelatedFileNotFoundError(CoreFileNotFoundError):
    """
    configuration related file not found error.
    """


class ConfigurationManager(CoreObject):
    """
    configuration manager class.
    """

    def __init__(self, **options):
        """
        initializes an instance of ConfigurationManager.
        """

        CoreObject.__init__(self)

        self._config_stores = {}
        self._settings_path = application_services.get_settings_path()

    def _load_all_configurations(self, settings_path):
        """
        loads all available configuration files from specified
        settings path into relevant config stores.

        :param str settings_path: settings directory full path.

        :raises ConfigurationSettingsPathNotExistedError: configuration settings
                                                          path not existed error.

        :raises ConfigurationRelatedFileNotFoundError: configuration related file
                                                       not found error.
        """

        for root, directories, file_names in os.walk(self._settings_path):
            files = [os.path.splitext(name)[0] for name in file_names]
            self.load_configurations(*files, silent=True)

    def _add_config_store(self, name, file_path):
        """
        adds a new config store for given file with the specified name.

        :param str name: config store name.
        :param str file_path: config file full path.

        :raises ConfigurationStoreExistedError: configuration store existed error.
        """

        if name in self._config_stores.keys():
            raise ConfigurationStoreExistedError('Config store with name [{name}] already '
                                                 'existed, config file names must be unique.'
                                                 .format(name=name))

        self._config_stores[name] = ConfigStore(name, file_path)

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

        :raises ConfigurationSettingsPathNotExistedError: configuration settings
                                                          path not existed error.

        :raises ConfigurationRelatedFileNotFoundError: configuration related file
                                                       not found error.
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

                self._add_config_store(single_file_name,
                                       os.path.join(self._settings_path,
                                                    single_file))
                return

        silent = options.get('silent', False)
        if silent is not True:
            raise ConfigurationRelatedFileNotFoundError('Config name [{name}] does not '
                                                        'have any related configuration '
                                                        'file in [{settings}].'
                                                        .format(name=name,
                                                                settings=self._settings_path))

    def load_configurations(self, *names, **options):
        """
        loads the given configurations if relevant files is
        available in settings path.

        :param str names: configuration names as arguments.

        :keyword bool silent: specifies that if a related configuration file
                              for any of the given names not found, ignore it.
                              otherwise raise an error. defaults to False.

        :raises ConfigurationSettingsPathNotExistedError: configuration settings
                                                          path not existed error.

        :raises ConfigurationRelatedFileNotFoundError: configuration related file
                                                       not found error.
        """

        for single_name in names:
            self.load_configuration(single_name, **options)

    def reload(self, store_name, **options):
        """
        reloads the configuration store from it's relevant file.

        :param str store_name: config store name to be reloaded.

        :raises ConfigurationStoreNotFoundError: configuration store not found error.
        """

        if store_name not in self._config_stores.keys():
            raise ConfigurationStoreNotFoundError('Config store [{name}] not found.'
                                                  .format(name=store_name))

        self._config_stores[store_name].reload(**options)

    def get_file_path(self, store_name):
        """
        gets the configuration file path for given store name.

        :param str store_name: config store name to get it's file path.

        :raises ConfigurationStoreNotFoundError: configuration store not found error.
        """

        if store_name not in self._config_stores.keys():
            raise ConfigurationStoreNotFoundError('Config store [{name}] not found.'
                                                  .format(name=store_name))

        return self._config_stores[store_name].get_file_path()

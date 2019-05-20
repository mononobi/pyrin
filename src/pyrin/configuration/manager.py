# -*- coding: utf-8 -*-
"""
configuration manager module.
"""

import os

import pyrin.application.services as application_services
from pyrin.configuration.store import ConfigStore

from pyrin.context import CoreObject
from pyrin.exceptions import CoreNotADirectoryError, CoreKeyError


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
        self._load_configurations(self._settings_path)

    def _load_configurations(self, settings_path):
        """
        loads all available configuration files from specified
        settings path into relevant config stores.

        :param settings_path: settings directory full path.
        """

        if not os.path.isdir(settings_path):
            raise CoreNotADirectoryError('Settings path [{path}] does not exist.'
                                         .format(path=settings_path))

        for root, directories, file_names in os.walk(self._settings_path):
            for file in file_names:
                if self._is_config_file(file):
                    self._add_config_store(os.path.splitext(file)[0],
                                           os.path.join(root, file))

            # for directory in directories:
            #     combined_path = os.path.join(root, directory)
            #     inner_files = os.listdir(combined_path)
            #     for inner_file in inner_files:
            #         self._add_config_store(os.path.splitext(file)[0],
            #                                os.path.join(root, file))

    def _add_config_store(self, name, file_path):
        """
        adds a new config store for given file with the specified name.

        :param str name: config store name.
        :param str file_path: config file full path.

        :raises CoreKeyError: core key error.
        """

        if name in self._config_stores.keys():
            raise CoreKeyError('Config store with name [{name}] already exists, '
                               'config file names must be unique.'
                               .format(name=name))

        self._config_stores[name] = ConfigStore(name, file_path)

    def _is_config_file(self, file_name):
        """
        gets a value indicating that given file name belongs to a config file.

        :param str file_name: file name.

        :rtype: bool
        """

        return file_name.endswith('.config')

# -*- coding: utf-8 -*-
"""
configuration services module.
"""

from pyrin.application.services import get_component
from pyrin.configuration import ConfigurationPackage


def load_configuration(name, **options):
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

    return get_component(ConfigurationPackage.COMPONENT_NAME).load_configuration(name,
                                                                                 **options)


def load_configurations(*names, **options):
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

    return get_component(ConfigurationPackage.COMPONENT_NAME).load_configurations(*names,
                                                                                  **options)


def reload(store_name, **options):
    """
    reloads the configuration store from it's relevant file.

    :param str store_name: config store name to be reloaded.

    :keyword dict defaults: a dict containing values
                            needed for interpolation.
                            defaults to None if not provided.

    :raises ConfigurationStoreNotFoundError: configuration store not found error.
    """

    return get_component(ConfigurationPackage.COMPONENT_NAME).reload(store_name, **options)


def get_file_path(store_name, **options):
    """
    gets the configuration file path for given config store.

    :param str store_name: config store name to get its file path.

    :keyword bool silent: specifies that if a related configuration file
                          for the given store name not found, ignore it.
                          otherwise raise an error. defaults to False.

    :raises ConfigurationFileNotFoundError: configuration file not found error.
    """

    return get_component(ConfigurationPackage.COMPONENT_NAME).get_file_path(store_name,
                                                                            **options)


def get_default_file_path(store_name, **options):
    """
    gets the default configuration file path for given config store.

    it gets the file path in `pyrin.settings.default` directory.
    if the file is not available, it could return None or raise an error.

    :param str store_name: config store name to get its file path.

    :keyword bool silent: specifies that if a related default configuration
                          file for the given store name not found, ignore it.
                          otherwise raise an error. defaults to False.

    :raises ConfigurationFileNotFoundError: configuration file not found error.
    """

    return get_component(ConfigurationPackage.COMPONENT_NAME).get_default_file_path(
        store_name, **options)


def get_file_name(store_name, **options):
    """
    gets the configuration file name for given config store.

    for example: `database.ini`

    :param str store_name: config store name to get its file name.

    :keyword bool silent: specifies that if a related configuration file
                          for the given store name not found, ignore it.
                          otherwise raise an error. defaults to False.

    :raises ConfigurationFileNotFoundError: configuration file not found error.
    """

    return get_component(ConfigurationPackage.COMPONENT_NAME).get_file_name(store_name,
                                                                            **options)


def create_config_files(*stores, **options):
    """
    creates the config files for given store names in application settings path.

    it creates the files based on files available in pyrin default settings.

    :param str stores: store names to create config file for them.

    :keyword bool replace_existing: specifies that it should replace file if a config
                                    file is already available for given store name.
                                    this argument takes precedence over
                                    `ignore_on_existed` argument.
                                    defaults to False if not provided.

    :keyword bool ignore_on_existed: specifies that if a config file for the
                                     store name is already existed, ignore
                                     it, otherwise raise an error.
                                     defaults to False if not provided.

    :keyword bool silent: specifies that if a related default configuration
                          file for the given store name not found, ignore it.
                          otherwise raise an error. defaults to False.

    :keyword dict[str, str] data: keyword with values to be replaced in config file.
                                  any keyword that does not exist in config file, will
                                  be ignored. defaults to None if not provided.

    :raises ConfigurationFileNotFoundError: configuration file not found error.
    :raises ConfigurationFileExistedError: configuration file existed error.
    """

    return get_component(ConfigurationPackage.COMPONENT_NAME).create_config_files(*stores,
                                                                                  **options)


def create_config_file(store, **options):
    """
    creates the config file for given store name in application settings path.

    it creates the file based on file available in pyrin default settings.

    :param str store: store name to create config file for it.

    :keyword bool replace_existing: specifies that it should replace file if a config
                                    file is already available for given store name.
                                    this argument takes precedence over
                                    `ignore_on_existed` argument.
                                    defaults to False if not provided.

    :keyword bool ignore_on_existed: specifies that if a config file for the
                                     store name is already existed, ignore
                                     it, otherwise raise an error.
                                     defaults to False if not provided.

    :keyword bool silent: specifies that if a related default configuration
                          file for the given store name not found, ignore it.
                          otherwise raise an error. defaults to False.

    :keyword dict[str, str] data: keyword with values to be replaced in config file.
                                  any keyword that does not exist in config file, will
                                  be ignored. defaults to None if not provided.

    :raises ConfigurationFileNotFoundError: configuration file not found error.
    :raises ConfigurationFileExistedError: configuration file existed error.
    """

    return get_component(ConfigurationPackage.COMPONENT_NAME).create_config_file(store,
                                                                                 **options)


def get(store_name, section, key, **options):
    """
    gets the value of specified key from provided section of given config store.

    :param str store_name: config store name.
    :param str section: config section name.
    :param str key: config key to get it's value.

    :keyword object default: default value if key not present in config section.
                             if not provided, error will be raised.

    :raises ConfigurationStoreNotFoundError: configuration store not found error.

    :raises ConfigurationStoreSectionNotFoundError: configuration store
                                                    section not found error.

    :raises ConfigurationStoreKeyNotFoundError: configuration store
                                                key not found error.
    """

    return get_component(ConfigurationPackage.COMPONENT_NAME).get(store_name, section,
                                                                  key, **options)


def get_active(store_name, key, **options):
    """
    gets the value of given key from active section of given config store.

    if this store does not have an active section, it raises an error.

    :param str store_name: config store name.
    :param str key: config key to get it's value.

    :keyword object default: default value if key not present in config section.
                             if not provided, error will be raised.

    :raises ConfigurationStoreNotFoundError: configuration store not found error.

    :raises ConfigurationStoreSectionNotFoundError: configuration store
                                                    section not found error.

    :raises ConfigurationStoreKeyNotFoundError: configuration store
                                                key not found error.
    """

    return get_component(ConfigurationPackage.COMPONENT_NAME).get_active(store_name,
                                                                         key, **options)


def get_section_names(store_name, **options):
    """
    gets all available section names of given config store.

    :param str store_name: config store name.

    :raises ConfigurationStoreNotFoundError: configuration store not found error.

    :rtype: list[str]
    """

    return get_component(ConfigurationPackage.COMPONENT_NAME).get_section_names(store_name,
                                                                                **options)


def get_section(store_name, section, **options):
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

    return get_component(ConfigurationPackage.COMPONENT_NAME).get_section(store_name, section,
                                                                          **options)


def get_section_keys(store_name, section, **options):
    """
    gets all available keys in given section of specified config store.

    :param str store_name: config store name.
    :param str section: section name.

    :raises ConfigurationStoreNotFoundError: configuration store not found error.

    :raises ConfigurationStoreSectionNotFoundError: configuration store section
                                                    not found error.

    :rtype: list[str]
    """

    return get_component(ConfigurationPackage.COMPONENT_NAME).get_section_keys(store_name,
                                                                               section,
                                                                               **options)


def get_all(store_name, **options):
    """
    gets all available key/values from different sections of given config store.

    in a flat dict, eliminating the sections.
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

    return get_component(ConfigurationPackage.COMPONENT_NAME).get_all(store_name, **options)


def get_active_section(store_name, **options):
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

    return get_component(ConfigurationPackage.COMPONENT_NAME).get_active_section(store_name,
                                                                                 **options)


def get_active_section_name(store_name):
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

    return get_component(ConfigurationPackage.COMPONENT_NAME).get_active_section_name(store_name)


def get_all_sections(store_name, **options):
    """
    gets all sections and their keys of given config store.

    :param str store_name: config store name.

    :raises ConfigurationStoreNotFoundError: configuration store not found error.

    :rtype: dict
    """

    return get_component(ConfigurationPackage.COMPONENT_NAME).get_all_sections(store_name,
                                                                               **options)

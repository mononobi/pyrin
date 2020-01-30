# -*- coding: utf-8 -*-
"""
configuration services module.
"""

from pyrin.application.services import get_component
from pyrin.configuration import ConfigurationPackage


def load_configuration(name, **options):
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

    return get_component(ConfigurationPackage.COMPONENT_NAME).load_configuration(name,
                                                                                 **options)


def load_configurations(*names, **options):
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

    return get_component(ConfigurationPackage.COMPONENT_NAME).load_configurations(*names,
                                                                                  **options)


def reload(store_name, **options):
    """
    reloads the configuration store from it's relevant file.

    :param str store_name: config store name to be reloaded.

    :raises ConfigurationStoreNotFoundError: configuration store not found error.
    """

    return get_component(ConfigurationPackage.COMPONENT_NAME).reload(store_name, **options)


def get_file_path(store_name, **options):
    """
    gets the configuration file path for given config store.

    :param str store_name: config store name to get it's file path.

    :raises ConfigurationStoreNotFoundError: configuration store not found error.
    """

    return get_component(ConfigurationPackage.COMPONENT_NAME).get_file_path(store_name,
                                                                            **options)


def get(store_name, section, key, **options):
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

    return get_component(ConfigurationPackage.COMPONENT_NAME).get(store_name, section,
                                                                  key, **options)


def get_active(store_name, key, **options):
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

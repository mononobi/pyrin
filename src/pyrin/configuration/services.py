# -*- coding: utf-8 -*-
"""
configuration services module.
"""

from pyrin.application.services import get_component
from pyrin.configuration.component import ConfigurationComponent


def load_configuration(name, **options):
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

    return get_component(ConfigurationComponent.COMPONENT_ID).load_configuration(name, **options)


def load_configurations(*names, **options):
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

    return get_component(ConfigurationComponent.COMPONENT_ID).\
        load_configurations(*names, **options)


def reload(store_name, **options):
    """
    reloads the configuration store from it's relevant file.

    :param str store_name: config store name to be reloaded.

    :raises ConfigurationStoreNotFoundError: configuration store not found error.
    """

    return get_component(ConfigurationComponent.COMPONENT_ID).reload(store_name, **options)

# -*- coding: utf-8 -*-
"""
configuration exceptions module.
"""

from pyrin.core.exceptions import CoreKeyError, CoreNotADirectoryError, CoreFileNotFoundError, \
    CoreValueError


class ConfigurationStoreNotFoundError(CoreKeyError):
    """
    configuration store not found error.
    """
    pass


class ConfigurationStoreExistedError(CoreKeyError):
    """
    configuration store existed error.
    """
    pass


class ConfigurationSettingsPathNotExistedError(CoreNotADirectoryError):
    """
    configuration settings path not existed error.
    """
    pass


class ConfigurationFileNotFoundError(CoreFileNotFoundError):
    """
    configuration file not found error.
    """
    pass


class ConfigurationStoreKeyNotFoundError(CoreKeyError):
    """
    configuration store key not found error.
    """
    pass


class ConfigurationStoreSectionNotFoundError(CoreKeyError):
    """
    configuration store section not found error.
    """
    pass


class ConfigurationStoreDuplicateKeyError(CoreKeyError):
    """
    configuration store duplicate key error.
    """
    pass


class ConfigurationEnvironmentVariableNotFoundError(CoreKeyError):
    """
    configuration environment variable not found error.
    """
    pass


class InvalidConfigurationEnvironmentVariableValueError(CoreValueError):
    """
    configuration environment variable value error.
    """
    pass

# -*- coding: utf-8 -*-
"""
configuration exceptions module.
"""

from pyrin.core.exceptions import CoreException


class ConfigurationManagerException(CoreException):
    """
    configuration manager exception.
    """
    pass


class ConfigurationStoreException(CoreException):
    """
    configuration store exception.
    """
    pass


class ConfigurationStoreNotFoundError(ConfigurationManagerException):
    """
    configuration store not found error.
    """
    pass


class ConfigurationStoreExistedError(ConfigurationManagerException):
    """
    configuration store existed error.
    """
    pass


class ConfigurationSettingsPathNotExistedError(ConfigurationManagerException):
    """
    configuration settings path not existed error.
    """
    pass


class ConfigurationFileNotFoundError(ConfigurationManagerException):
    """
    configuration file not found error.
    """
    pass


class ConfigurationStoreKeyNotFoundError(ConfigurationStoreException):
    """
    configuration store key not found error.
    """
    pass


class ConfigurationStoreSectionNotFoundError(ConfigurationStoreException):
    """
    configuration store section not found error.
    """
    pass


class ConfigurationStoreDuplicateKeyError(ConfigurationStoreException):
    """
    configuration store duplicate key error.
    """
    pass


class ConfigurationEnvironmentVariableNotFoundError(ConfigurationStoreException):
    """
    configuration environment variable not found error.
    """
    pass


class InvalidConfigurationEnvironmentVariableValueError(ConfigurationStoreException):
    """
    configuration environment variable value error.
    """
    pass

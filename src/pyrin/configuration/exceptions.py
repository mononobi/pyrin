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


class ConfigurationStoreException(ConfigurationManagerException):
    """
    configuration store exception.
    """
    pass


class ConfigurationStoreAttributeNotFoundException(ConfigurationStoreException):
    """
    configuration store attribute not found exception.
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


class ConfigurationFileNotFoundError(ConfigurationManagerException):
    """
    configuration file not found error.
    """
    pass


class ConfigurationStoreKeyNotFoundError(ConfigurationStoreAttributeNotFoundException):
    """
    configuration store key not found error.
    """
    pass


class ConfigurationStoreSectionNotFoundError(ConfigurationStoreAttributeNotFoundException):
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


class ConfigurationFileExistedError(ConfigurationManagerException):
    """
    configuration file existed error.
    """
    pass


class InvalidPlaceHolderForEnvironmentVariableError(ConfigurationStoreException):
    """
    invalid place holder for environment variable error.
    """
    pass


class InvalidEnvironmentVariableKeyError(ConfigurationStoreException):
    """
    invalid environment variable key error.
    """
    pass

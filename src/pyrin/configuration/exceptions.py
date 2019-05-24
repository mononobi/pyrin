# -*- coding: utf-8 -*-
"""
configuration exceptions module.
"""

from pyrin.exceptions import CoreKeyError, CoreNotADirectoryError, CoreFileNotFoundError


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


class ConfigurationStoreSectionOrKeyNotFoundError(CoreKeyError):
    """
    configuration store section or key not found error.
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

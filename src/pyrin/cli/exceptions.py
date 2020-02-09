# -*- coding: utf-8 -*-
"""
cli exceptions module.
"""

from pyrin.core.exceptions import CoreException


class CLIManagerException(CoreException):
    """
    cli manager exception.
    """
    pass


class MetaDataOptionsParamNameIsRequiredError(CLIManagerException):
    """
    metadata options param name is required error.
    """
    pass


class ParamValueIsNotMappedToCLIError(CLIManagerException):
    """
    param value is not mapped to cli error.
    """
    pass


class InvalidCLIHandlerNameError(CLIManagerException):
    """
    invalid cli handler name error.
    """
    pass

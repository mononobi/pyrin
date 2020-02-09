# -*- coding: utf-8 -*-
"""
cli exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class CLIManagerException(CoreException):
    """
    cli manager exception.
    """
    pass


class CLIManagerBusinessException(CoreBusinessException, CLIManagerException):
    """
    cli manager business exception.
    """
    pass


class MetaDataOptionsParamNameIsRequiredError(CLIManagerException):
    """
    metadata options param name is required error.
    """
    pass


class ParamValueIsNotMappedToCLIError(CLIManagerBusinessException):
    """
    param value is not mapped to cli error.
    """
    pass


class InvalidCLIHandlerNameError(CLIManagerException):
    """
    invalid cli handler name error.
    """
    pass


class InvalidCLIHandlerTypeError(CLIManagerException):
    """
    invalid cli handler type error.
    """
    pass


class DuplicatedCLIHandlerError(CLIManagerException):
    """
    duplicated cli handler error.
    """
    pass


class CLIHandlerNotFoundError(CLIManagerBusinessException):
    """
    cli handler not found error.
    """
    pass

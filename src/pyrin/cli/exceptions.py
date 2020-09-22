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


class ArgumentParamNameIsRequiredError(CLIManagerException):
    """
    argument param name is required error.
    """
    pass


class PositionalArgumentIndexError(CLIManagerException):
    """
    positional argument index error.
    """
    pass


class BooleanArgumentValueError(CLIManagerException):
    """
    boolean argument value error.
    """
    pass


class KeywordArgumentCLIOptionNameError(CLIManagerException):
    """
    keyword argument cli option name error.
    """
    pass


class MappingArgumentParamValueToCLIMapRequiredError(CLIManagerException):
    """
    mapping argument param value to cli map required error.
    """
    pass


class KeywordArgumentCLIOptionNameRequiredError(CLIManagerException):
    """
    keyword argument cli option name required error.
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


class PositionalArgumentsIndicesError(CLIManagerException):
    """
    positional arguments indices error.
    """
    pass


class InvalidCLIDecoratedMethodError(CLIManagerException):
    """
    invalid cli decorated method error.
    """
    pass


class InvalidCLIParamTypeError(CLIManagerException):
    """
    invalid cli param type error.
    """
    pass


class DuplicatedCLIGroupError(CLIManagerException):
    """
    duplicated cli group error.
    """
    pass


class InvalidCLIGroupTypeError(CLIManagerException):
    """
    invalid cli group type error.
    """
    pass


class CLIGroupNameIsRequiredError(CLIManagerException):
    """
    cli group name is required error.
    """
    pass

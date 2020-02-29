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


class ArgumentMetadataParamNameIsRequiredError(CLIManagerException):
    """
    argument metadata param name is required error.
    """
    pass


class PositionalArgumentMetadataIndexError(CLIManagerException):
    """
    positional argument metadata index error.
    """
    pass


class BooleanArgumentMetadataValueError(CLIManagerException):
    """
    boolean argument metadata value error.
    """
    pass


class KeywordArgumentMetadataCLIOptionNameError(CLIManagerException):
    """
    keyword argument metadata cli option name error.
    """
    pass


class MappingArgumentMetadataParamValueToCLIMapRequiredError(CLIManagerException):
    """
    mapping argument metadata param value to cli map required error.
    """
    pass


class KeywordArgumentMetadataCLIOptionNameRequiredError(CLIManagerException):
    """
    keyword argument metadata cli option name required error.
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


class InvalidArgumentMetaDataTypeError(CLIManagerException):
    """
    invalid argument metadata type error.
    """
    pass


class PositionalArgumentsIndicesError(CLIManagerException):
    """
    positional arguments indices error.
    """
    pass

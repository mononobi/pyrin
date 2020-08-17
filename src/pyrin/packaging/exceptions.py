# -*- coding: utf-8 -*-
"""
packaging exceptions module.
"""

from pyrin.core.exceptions import CoreException


class PackagingManagerException(CoreException):
    """
    packaging manager exception.
    """
    pass


class InvalidPackageNameError(PackagingManagerException):
    """
    invalid package name error.
    """
    pass


class ComponentModuleNotFoundError(PackagingManagerException):
    """
    component module not found error.
    """
    pass


class BothUnitAndIntegrationTestsCouldNotBeLoadedError(PackagingManagerException):
    """
    both unit and integration tests could not be loaded error.
    """
    pass


class InvalidPackagingHookTypeError(PackagingManagerException):
    """
    invalid packaging hook type error.
    """
    pass


class CircularDependencyDetectedError(PackagingManagerException):
    """
    circular dependency detected error.
    """
    pass


class SelfDependencyDetectedError(PackagingManagerException):
    """
    self dependency detected error.
    """
    pass


class SubPackageDependencyDetectedError(PackagingManagerException):
    """
    sub-package dependency detected error.
    """
    pass


class PackageExternalDependencyError(PackagingManagerException):
    """
    package external dependency error.
    """
    pass


class PackageNotExistedError(PackagingManagerException):
    """
    package not existed error.
    """
    pass


class PackageIsIgnoredError(PackagingManagerException):
    """
    package is ignored error.
    """
    pass


class PackageIsDisabledError(PackagingManagerException):
    """
    package is disabled error.
    """
    pass

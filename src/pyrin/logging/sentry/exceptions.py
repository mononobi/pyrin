# -*- coding: utf-8 -*-
"""
sentry exceptions module.
"""

from pyrin.core.exceptions import CoreException


class SentryManagerException(CoreException):
    """
    sentry manager exception.
    """
    pass


class SentryIntegrationNotFoundError(SentryManagerException):
    """
    sentry integration not found error.
    """
    pass


class InvalidSentryIntegrationTypeError(SentryManagerException):
    """
    invalid sentry integration type error.
    """
    pass


class DuplicatedSentryIntegrationError(SentryManagerException):
    """
    duplicated sentry integration error.
    """
    pass

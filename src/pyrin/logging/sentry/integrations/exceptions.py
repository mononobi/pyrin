# -*- coding: utf-8 -*-
"""
sentry integrations exceptions module.
"""

from pyrin.core.exceptions import CoreException


class SentryIntegrationsException(CoreException):
    """
    sentry integrations exception.
    """
    pass


class SentryIntegrationNameRequiredError(SentryIntegrationsException):
    """
    sentry integration name required error.
    """
    pass

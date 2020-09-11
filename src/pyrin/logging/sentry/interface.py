# -*- coding: utf-8 -*-
"""
sentry interface module.
"""

from abc import abstractmethod
from threading import Lock

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.core.structs import CoreObject, MultiSingletonMeta


class SentryIntegrationSingletonMeta(MultiSingletonMeta):
    """
    sentry integration singleton meta class.

    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class AbstractSentryIntegration(CoreObject, metaclass=SentryIntegrationSingletonMeta):
    """
    abstract sentry integration class.

    all application sentry integrations must be subclassed from this.
    """

    @abstractmethod
    def configure(self, integrations, **options):
        """
        configures this integration.

        :param list[Integration] integrations: list of enabled integrations.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def is_enabled(self):
        """
        gets a value indicating that this integration is enabled in sentry config store.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

# -*- coding: utf-8 -*-
"""
sentry integrations base module.
"""

from abc import abstractmethod

import pyrin.configuration.services as config_services

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.logging.sentry.interface import AbstractSentryIntegration
from pyrin.logging.sentry.integrations.exceptions import SentryIntegrationNameRequiredError


class SentryIntegrationBase(AbstractSentryIntegration):
    """
    sentry integration base class.

    all application sentry integrations must be subclassed from this.
    """

    # name of the integration. each subclass must set this to a valid name.
    name = None

    def __init__(self, *args, **options):
        """
        initializes an instance of SentryIntegrationBase.

        :raises SentryIntegrationNameRequiredError: sentry integration name required error.
        """

        super().__init__()

        if self.name in (None, '') or self.name.isspace():
            raise SentryIntegrationNameRequiredError('Sentry integration name is required '
                                                     'for integration [{instance}].'
                                                     .format(instance=self))

        self._set_name(self.name)

    def configure(self, integrations, **options):
        """
        configures this integration.

        :param list[Integration] integrations: list of enabled integrations.
        """

        if self.is_enabled is not True:
            return

        config = self._configure(**options)
        integrations.append(config)

    @abstractmethod
    def _configure(self, **options):
        """
        configures this integration and gets the configured object.

        this method must be overridden in subclasses.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: Integration
        """

        raise CoreNotImplementedError()

    @property
    def is_enabled(self):
        """
        gets a value indicating that this integration is enabled in sentry config store.

        :rtype: bool
        """

        enabled = config_services.get('sentry', self.get_name(), 'enable')
        return enabled is True

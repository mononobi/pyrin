# -*- coding: utf-8 -*-
"""
sentry integrations logging module.
"""

from sentry_sdk.integrations.logging import LoggingIntegration

import pyrin.configuration.services as config_services

from pyrin.logging.sentry.decorators import sentry_integration
from pyrin.logging.sentry.integrations.base import SentryIntegrationBase


@sentry_integration()
class LoggingSentryIntegration(SentryIntegrationBase):
    """
    logging sentry integration class.
    """

    name = 'logging'

    def _configure(self, **options):
        """
        configures this integration and gets the configured object.

        :rtype: LoggingIntegration
        """

        level = config_services.get('sentry', self.get_name(), 'level')
        event_level = config_services.get('sentry', self.get_name(), 'event_level')
        return LoggingIntegration(level, event_level)

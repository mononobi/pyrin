# -*- coding: utf-8 -*-
"""
sentry integrations celery module.
"""

import pyrin.configuration.services as config_services

from pyrin.logging.sentry.decorators import sentry_integration
from pyrin.logging.sentry.integrations.base import SentryIntegrationBase


@sentry_integration()
class CelerySentryIntegration(SentryIntegrationBase):
    """
    celery sentry integration class.
    """

    name = 'celery'

    def _configure(self, **options):
        """
        configures this integration and gets the configured object.

        :rtype: CeleryIntegration
        """

        # we have to import CeleryIntegration here, because sentry imports celery
        # at the module level and raises an error if it isn't installed.
        from sentry_sdk.integrations.celery import CeleryIntegration

        propagate_traces = config_services.get('sentry', self.get_name(), 'propagate_traces')
        return CeleryIntegration(propagate_traces)

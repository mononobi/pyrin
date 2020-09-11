# -*- coding: utf-8 -*-
"""
sentry integrations flask module.
"""

from sentry_sdk.integrations.flask import FlaskIntegration

import pyrin.configuration.services as config_services

from pyrin.logging.sentry.decorators import sentry_integration
from pyrin.logging.sentry.integrations.base import SentryIntegrationBase


@sentry_integration()
class FlaskSentryIntegration(SentryIntegrationBase):
    """
    flask sentry integration class.
    """

    name = 'flask'

    def _configure(self, **options):
        """
        configures this integration and gets the configured object.

        :rtype: FlaskIntegration
        """

        transaction_style = config_services.get('sentry', self.get_name(), 'transaction_style')
        return FlaskIntegration(transaction_style)

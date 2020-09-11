# -*- coding: utf-8 -*-
"""
sentry integrations redis module.
"""

from sentry_sdk.integrations.redis import RedisIntegration

from pyrin.logging.sentry.decorators import sentry_integration
from pyrin.logging.sentry.integrations.base import SentryIntegrationBase


@sentry_integration()
class RedisSentryIntegration(SentryIntegrationBase):
    """
    redis sentry integration class.
    """

    name = 'redis'

    def _configure(self, **options):
        """
        configures this integration and gets the configured object.

        :rtype: RedisIntegration
        """

        return RedisIntegration()

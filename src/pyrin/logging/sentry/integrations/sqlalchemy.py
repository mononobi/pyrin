# -*- coding: utf-8 -*-
"""
sentry integrations sqlalchemy module.
"""

from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from pyrin.logging.sentry.decorators import sentry_integration
from pyrin.logging.sentry.integrations.base import SentryIntegrationBase


@sentry_integration()
class SQLAlchemySentryIntegration(SentryIntegrationBase):
    """
    sqlalchemy sentry integration class.
    """

    name = 'sqlalchemy'

    def _configure(self, **options):
        """
        configures this integration and gets the configured object.

        :rtype: SqlalchemyIntegration
        """

        return SqlalchemyIntegration()

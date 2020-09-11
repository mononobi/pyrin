# -*- coding: utf-8 -*-
"""
sentry services module.
"""

from pyrin.application.services import get_component
from pyrin.logging.sentry import SentryPackage


def register_integration(instance, **options):
    """
    registers a new integration or replaces the existing one.

    if `replace=True` is provided. otherwise, it raises an error
    on adding an integration which is already registered.

    :param AbstractSentryIntegration instance: integration instance to be registered.

    :keyword bool replace: specifies that if there is another registered
                           integration with the same name, replace it with the
                           new one, otherwise raise an error. defaults to False.

    :raises InvalidSentryIntegrationTypeError: invalid sentry integration type error.
    :raises DuplicatedSentryIntegrationError: duplicated sentry integration error.
    """

    get_component(SentryPackage.COMPONENT_NAME).register_integration(instance, **options)


def configure(**options):
    """
    configures sentry client and all enabled integrations.
    """

    get_component(SentryPackage.COMPONENT_NAME).configure(**options)


def try_report_exception(error, **options):
    """
    tries to report exception to sentry server.

    if logging integration is not enabled to send it automatically.

    :param Exception error: exception instance that has been occurred.
    """

    get_component(SentryPackage.COMPONENT_NAME).try_report_exception(error, **options)

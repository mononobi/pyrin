# -*- coding: utf-8 -*-
"""
sentry decorators module.
"""

import pyrin.logging.sentry.services as sentry_services


def sentry_integration(*args, **kwargs):
    """
    decorator to register a sentry integration.

    :param object args: integration class constructor arguments.
    :param object kwargs: integration class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           integration with the same name, replace it with
                           the new one. otherwise raise an error.
                           defaults to False.

    :raises InvalidSentryIntegrationTypeError: invalid sentry integration type error.
    :raises DuplicatedSentryIntegrationError: duplicated sentry integration error.

    :returns: integration class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available sentry integrations.

        :param type cls: integration class.

        :returns: integration class.
        :rtype: type
        """

        instance = cls(*args, **kwargs)
        sentry_services.register_integration(instance, **kwargs)

        return cls

    return decorator

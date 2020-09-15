# -*- coding: utf-8 -*-
"""
sentry manager module.
"""

import sentry_sdk

import pyrin.configuration.services as config_services

from pyrin.caching.mixin.decorators import fast_cache
from pyrin.caching.mixin.typed import TypedCacheMixin
from pyrin.core.structs import Manager, Context
from pyrin.logging.enumerations import LogLevelEnum, LogLevelIntEnum
from pyrin.logging.sentry import SentryPackage
from pyrin.logging.sentry.interface import AbstractSentryIntegration
from pyrin.utils.custom_print import print_warning
from pyrin.logging.sentry.exceptions import InvalidSentryIntegrationTypeError, \
    DuplicatedSentryIntegrationError, SentryIntegrationNotFoundError


class SentryManager(Manager, TypedCacheMixin):
    """
    sentry manager class.
    """

    package_class = SentryPackage

    def __init__(self):
        """
        initializes an instance of SentryManager.
        """

        super().__init__()

        # a dict containing different integrations in the form of:
        # {str name: AbstractSentryIntegration integration}
        self._integrations = Context()

    def _get_integration(self, name):
        """
        gets the registered integration with given name.

        it raises an error if no integration found for given name.

        :param str name: name of the integration to be get.

        :raises SentryIntegrationNotFoundError: sentry integration not found error.

        :rtype: AbstractSentryIntegration
        """

        if name not in self._integrations:
            raise SentryIntegrationNotFoundError('Sentry integration [{name}] does '
                                                 'not exist.'.format(name=name))

        return self._integrations.get(name)

    @fast_cache
    def _is_logging_integration_enabled(self):
        """
        gets a value indicating that logging integration is enabled.

        :rtype: bool
        """

        default_integrations_enabled = config_services.get_active('sentry',
                                                                  'default_integrations')

        logging_enabled = config_services.get('sentry', 'logging', 'enable')
        logging_event_level = config_services.get('sentry', 'logging', 'event_level')

        return (default_integrations_enabled is True and logging_enabled is False) or \
               (logging_enabled is True and logging_event_level in (LogLevelEnum.ERROR,
                                                                    LogLevelEnum.WARNING,
                                                                    LogLevelEnum.INFO,
                                                                    LogLevelEnum.DEBUG,
                                                                    LogLevelIntEnum.ERROR,
                                                                    LogLevelIntEnum.WARNING,
                                                                    LogLevelIntEnum.INFO,
                                                                    LogLevelIntEnum.DEBUG))

    def register_integration(self, instance, **options):
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

        if not isinstance(instance, AbstractSentryIntegration):
            raise InvalidSentryIntegrationTypeError('Input parameter [{instance}] is '
                                                    'not an instance of [{base}].'
                                                    .format(instance=instance,
                                                            base=AbstractSentryIntegration))

        if instance.get_name() in self._integrations:
            old_instance = self._get_integration(instance.get_name())
            replace = options.get('replace', False)
            if replace is not True:
                raise DuplicatedSentryIntegrationError('There is another registered sentry '
                                                       'integration [{old}] with name [{name}] '
                                                       'but "replace" option is not set, so '
                                                       'integration [{instance}] could not be '
                                                       'registered.'
                                                       .format(old=old_instance,
                                                               name=instance.get_name(),
                                                               instance=instance))

            print_warning('Sentry integration [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=old_instance,
                                  new_instance=instance))

        self._integrations[instance.get_name()] = instance

    def configure(self, **options):
        """
        configures sentry client and all enabled integrations.
        """

        integrations = []
        for name, instance in self._integrations.items():
            instance.configure(integrations)

        configs = config_services.get_active_section('sentry')
        sentry_sdk.init(**configs, integrations=integrations)

    def try_report_exception(self, error, **options):
        """
        tries to report exception to sentry server.

        if logging integration is not enabled to send it automatically.

        :param Exception error: exception instance that has been occurred.
        """

        if self._is_logging_integration_enabled() is False:
            sentry_sdk.capture_exception(error)

# -*- coding: utf-8 -*-
"""
sentry hooks module.
"""

import pyrin.logging.sentry.services as sentry_services

from pyrin.api.decorators import api_hook
from pyrin.api.hooks import APIHookBase
from pyrin.logging.sentry.integrations import SentryIntegrationsPackage
from pyrin.packaging.decorators import packaging_hook
from pyrin.packaging.hooks import PackagingHookBase


@packaging_hook()
class PackagingHook(PackagingHookBase):
    """
    packaging hook class.
    """

    def package_loaded(self, package_name, **options):
        """
        this method will be called after each application package has been loaded.

        :param str package_name: name of the loaded package.
        """

        # we should call this method as soon as integrations package is
        # loaded, to make sure sentry configures itself on time.
        if package_name == SentryIntegrationsPackage.NAME:
            sentry_services.configure()


@api_hook()
class APIHook(APIHookBase):
    """
    api hook class.
    """

    def exception_occurred(self, error, **options):
        """
        this method will be called when an exception is occurred.

        :param Exception error: exception instance that has been occurred.
        """

        sentry_services.try_report_exception(error, **options)

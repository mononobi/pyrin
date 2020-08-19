# -*- coding: utf-8 -*-
"""
database hooks module.
"""

import pyrin.database.services as database_services

from pyrin.application.decorators import application_hook
from pyrin.application.hooks import ApplicationHookBase
from pyrin.core.structs import Hook
from pyrin.packaging.decorators import packaging_hook
from pyrin.packaging.hooks import PackagingHookBase


class DatabaseHookBase(Hook):
    """
    database hook base class.
    """

    def after_session_factories_configured(self):
        """
        this method will be called after all database session factories have been configured.
        """
        pass


@packaging_hook()
class PackagingHook(PackagingHookBase):
    """
    packaging hook class.
    """

    def after_packages_loaded(self):
        """
        this method will be called after all application packages have been loaded.
        """

        # we have to configure session factories after all models have
        # been loaded to enable multiple database connections if needed.
        database_services.configure_session_factories()


@application_hook()
class ApplicationHook(ApplicationHookBase):
    """
    application hook class.
    """

    def finalize_transaction(self, response, **options):
        """
        this method will be called after a request has been fully processed.

        :param CoreResponse response: response object.

        :rtype: CoreResponse
        """

        return database_services.finalize_transaction(response, **options)

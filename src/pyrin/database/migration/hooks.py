# -*- coding: utf-8 -*-
"""
database migration hooks module.
"""

import pyrin.database.migration.services as migration_services

from pyrin.application.decorators import application_hook
from pyrin.application.hooks import ApplicationHookBase
from pyrin.database.decorators import database_hook
from pyrin.database.hooks import DatabaseHookBase


@database_hook()
class DatabaseHook(DatabaseHookBase):
    """
    database hook class.
    """

    def after_session_factories_configured(self):
        """
        this method will be called after all database session factories have been configured.
        """

        migration_services.configure_migration_data()


@application_hook()
class ApplicationHook(ApplicationHookBase):
    """
    application hook class.
    """

    def after_application_loaded(self):
        """
        this method will be called after application has been loaded.
        """

        migration_services.rebuild_schema()

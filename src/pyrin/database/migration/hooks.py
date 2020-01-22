# -*- coding: utf-8 -*-
"""
database hooks module.
"""

import pyrin.database.migration.services as migration_services
import pyrin.configuration.services as config_services

from pyrin.application.decorators import application_hook
from pyrin.application.hooks import ApplicationHookBase
from pyrin.database.decorators import database_hook
from pyrin.database.hooks import DatabaseHookBase
from pyrin.utils.custom_print import print_warning, print_info


@database_hook()
class DatabaseHook(DatabaseHookBase):
    """
    database hook class.
    """

    def __init__(self):
        """
        initializes an instance of DatabaseHook.
        """

        DatabaseHookBase.__init__(self)

    def after_session_factories_configured(self):
        """
        this method will be called after all database
        session factories have been configured.
        """

        migration_services.configure_migration_data()


@application_hook()
class ApplicationHook(ApplicationHookBase):
    """
    application hook class.
    """

    def __init__(self):
        """
        initializes an instance of ApplicationHook.
        """

        ApplicationHookBase.__init__(self)

    def after_application_loaded(self):
        """
        this method will be called after application has been loaded.
        """

        # we should check whether it is required to drop
        # all entities in database on server startup.
        if config_services.get('database', 'migration', 'drop_on_startup') is True:
            environment = config_services.get_active('environment', 'env')
            debug = config_services.get_active('environment', 'debug')
            unit_testing = config_services.get_active('environment', 'unit_testing')

            if (environment == 'development' and debug is True) or \
                    (environment == 'testing' and unit_testing is True):
                print_warning('Dropping all models...')
                migration_services.drop_all()

        # we should check whether it is required to create
        # all entities in database on server startup.
        if config_services.get('database', 'migration', 'create_on_startup') is True:
            print_info('Creating all models...')
            migration_services.create_all()

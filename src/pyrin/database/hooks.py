# -*- coding: utf-8 -*-
"""
database hooks module.
"""

import pyrin.database.services as database_services
import pyrin.configuration.services as config_services

from pyrin.application.decorators import application_hook
from pyrin.application.hooks import ApplicationHookBase
from pyrin.packaging.decorators import packaging_hook
from pyrin.packaging.hooks import PackagingHookBase
from pyrin.utils.custom_print import print_warning, print_info


@packaging_hook()
class PackagingHook(PackagingHookBase):
    """
    packaging hook class.
    """

    def __init__(self):
        """
        initializes an instance of PackagingHook.
        """

        PackagingHookBase.__init__(self)

    def after_packages_loaded(self):
        """
        this method will be called after all application packages has been loaded.
        """

        # we have to configure session factories after all models have
        # been loaded to enable multiple database connections if needed.
        database_services.configure_session_factories()


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
        if config_services.get('database', 'general', 'drop_on_startup') is True:
            environment = config_services.get_active('environment', 'env')
            debug = config_services.get_active('environment', 'debug')
            unit_testing = config_services.get_active('environment', 'unit_testing')

            if (environment == 'development' and debug is True) or \
                    (environment == 'testing' and unit_testing is True):
                print_warning('Dropping all models...')
                database_services.drop_all()

        # we should check whether it is required to create
        # all entities in database on server startup.
        if config_services.get('database', 'general', 'create_on_startup') is True:
            print_info('Creating all models...')
            database_services.create_all()

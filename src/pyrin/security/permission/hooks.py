# -*- coding: utf-8 -*-
"""
permission hooks module.
"""

import pyrin.security.permission.services as permission_services
import pyrin.configuration.services as configs_services

from pyrin.application.decorators import application_hook
from pyrin.application.hooks import ApplicationHookBase
from pyrin.utils.custom_print import print_info


@application_hook()
class ApplicationHook(ApplicationHookBase):
    """
    application hook class.
    """

    def prepare_runtime_data(self):
        """
        this method will be get called after application has been fully initialized.

        any changes of this method to database, will be committed automatically by
        application. so you should not commit anything in the hook. if you do commit
        manually, unexpected behaviors may occur.

        note that this method will not get called when application starts in scripting mode.
        """

        synchronize = configs_services.get('security', 'permission', 'synchronize')
        if synchronize is True:
            print_info('Synchronizing permissions...')
            permission_services.synchronize_all()

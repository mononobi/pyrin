# -*- coding: utf-8 -*-
"""
permission hooks module.
"""

import pyrin.security.permission.services as permission_services

from pyrin.application.decorators import application_hook
from pyrin.application.hooks import ApplicationHookBase


@application_hook()
class ApplicationHook(ApplicationHookBase):
    """
    application hook class.
    """

    def __init__(self):
        """
        initializes an instance of ApplicationHook.
        """

        super().__init__()

    def prepare_runtime_data(self):
        """
        this method will be get called after application has been fully initialized.

        note that this method will not get called when
        application starts in scripting mode.
        """

        # we should synchronize all application permissions with database.
        permission_services.synchronize_all()

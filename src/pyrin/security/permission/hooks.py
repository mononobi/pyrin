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

        ApplicationHookBase.__init__(self)

    def before_application_start(self):
        """
        this method will be called before application gets started.
        """

        # we should synchronize all application permissions with database.
        permission_services.synchronize_all()

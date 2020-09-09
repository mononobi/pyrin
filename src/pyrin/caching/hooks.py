# -*- coding: utf-8 -*-
"""
caching hooks module.
"""

import pyrin.caching.services as caching_services

from pyrin.application.decorators import application_hook
from pyrin.application.enumerations import ApplicationStatusEnum
from pyrin.application.hooks import ApplicationHookBase


@application_hook()
class ApplicationHook(ApplicationHookBase):
    """
    application hook class.
    """

    def application_status_changed(self, old_status, new_status):
        """
        this method will be called whenever application status changes.

        :param str old_status: old application status.
        :param str new_status: new application status.

        :enum status:
            INITIALIZING = 'Initializing'
            LOADING = 'Loading'
            READY = 'Ready'
            RUNNING = 'Running'
            TERMINATED = 'Terminated'
        """

        if new_status == ApplicationStatusEnum.TERMINATED:
            caching_services.persist_all(clear=True)

    def prepare_runtime_data(self):
        """
        this method will be get called after application has been fully initialized.

        any changes of this method to database, will be committed automatically by
        application. so you should not commit anything in the hook. if you do commit
        manually, unexpected behaviors may occur.

        note that this method will not get called when application starts in scripting mode.
        """

        caching_services.load_all()

    def after_application_loaded(self):
        """
        this method will be called after application has been loaded.
        """

        caching_services.clear_required_caches()

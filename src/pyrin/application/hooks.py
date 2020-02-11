# -*- coding: utf-8 -*-
"""
application hooks module.
"""

from pyrin.core.context import Hook


class ApplicationHookBase(Hook):
    """
    application hook base class.
    all packages that need to be hooked into application business must
    implement this class and register it in application hooks.
    """

    def __init__(self):
        """
        initializes an instance of ApplicationHookBase.
        """

        super().__init__()

    def after_application_loaded(self):
        """
        this method will be called after application has been loaded.
        """
        pass

    def before_application_start(self):
        """
        this method will be called before application gets started.
        note that this method will not get called when application
        starts in scripting mode.
        """
        pass

    def application_status_changed(self, old_status, new_status):
        """
        this method will be called whenever application status changes.

        :param str old_status: old application status.
        :param str new_status: new application status.

        :note status:
            INITIALIZING = 'Initializing'
            LOADING = 'Loading'
            RUNNING = 'Running'
            TERMINATED = 'Terminated'
        """
        pass

# -*- coding: utf-8 -*-
"""
audit hooks module.
"""

import pyrin.audit.services as audit_services
import pyrin.configuration.services as config_services

from pyrin.core.structs import Hook
from pyrin.utils.custom_print import print_info
from pyrin.application.decorators import application_hook
from pyrin.application.hooks import ApplicationHookBase


class AuditHookBase(Hook):
    """
    audit hook base class.

    all packages that need to be hooked into audit business must
    implement this class and register it in audit hooks.
    """

    # name of the current audit, for example: database or celery.
    # the result of each audit will be added to final result dict using this key.
    audit_name = None

    def inspect(self, **options):
        """
        this method will be called to inspect the status of a package or resource.

        each subclass must return a tuple of two values. first value is a dict
        containing the inspection data. and the second value is a bool value
        indicating that inspection has been succeeded or failed.

        subclasses could also raise an exception instead of returning a value to
        indicate the failure, if required.

        :keyword bool traceback: specifies that on failure report, it must include
                                 the traceback of errors.
                                 defaults to True if not provided.

        :keyword bool raise_error: specifies that it must raise error
                                   if any of registered audits failed
                                   instead of returning a failure response.
                                   defaults to False if not provided.

        :rtype: tuple[dict, bool]
        """

        return {}, True


@application_hook()
class ApplicationHook(ApplicationHookBase):
    """
    application hook class.
    """

    def before_application_run(self):
        """
        this method will be get called just before application gets running.

        note that this method will not get called when
        application starts in scripting mode.

        :raises AuditFailedError: audit failed error.
        """

        startup_audit = config_services.get_active('audit', 'startup_audit')
        if startup_audit is True:
            print_info('Performing audit...')
            audit_services.startup_inspect()

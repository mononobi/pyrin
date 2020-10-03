# -*- coding: utf-8 -*-
"""
database audit hooks module.
"""

import pyrin.database.audit.services as database_audit_services

from pyrin.audit.decorators import audit_hook
from pyrin.audit.hooks import AuditHookBase


@audit_hook()
class AuditHook(AuditHookBase):
    """
    audit hook class.
    """

    audit_name = 'database'

    def inspect(self, **options):
        """
        this method will be called to inspect the status of a package or resource.

        it returns a tuple of two values. first value is a dict containing the inspection
        data. and the second value is a bool value indicating that inspection has been
        succeeded or failed.

        :keyword bool traceback: specifies that on failure report, it must include
                                 the traceback of errors.
                                 defaults to True if not provided.

        :keyword bool raise_error: specifies that it must raise error
                                   if any of registered audits failed
                                   instead of returning a failure response.
                                   defaults to False if not provided.

        :rtype: tuple[dict, bool]
        """

        return database_audit_services.inspect(**options)

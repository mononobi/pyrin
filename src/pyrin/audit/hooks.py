# -*- coding: utf-8 -*-
"""
audit hooks module.
"""

from pyrin.core.structs import Hook


class AuditHookBase(Hook):
    """
    audit hook base class.

    all packages that need to be hooked into audit business must
    implement this class and register it in audit hooks.
    """

    # name of the current audit, for example: database or celery.
    audit_name = None

    def inspect(self, **options):
        """
        this method will be called to inspect the status of a package or resource.

        each subclass must return a dict containing the inspection data.

        :rtype: dict
        """

        return {}

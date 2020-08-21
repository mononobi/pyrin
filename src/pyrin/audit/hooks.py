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

        :rtype: tuple[dict, bool]
        """

        return {}, True

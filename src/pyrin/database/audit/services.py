# -*- coding: utf-8 -*-
"""
database audit services module.
"""

from pyrin.application.services import get_component
from pyrin.database.audit import DatabaseAuditPackage


def inspect(**options):
    """
    inspects the status of available databases.

    it returns a tuple of two values. first value is a dict containing the inspection
    data. and the second value is a bool value indicating that inspection has been
    succeeded or failed.

    :keyword bool traceback: specifies that on failure report, it must include
                             the traceback of errors.
                             defaults to True if not provided.

    :rtype: tuple[dict, bool]
    """

    return get_component(DatabaseAuditPackage.COMPONENT_NAME).inspect(**options)

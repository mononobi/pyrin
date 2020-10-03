# -*- coding: utf-8 -*-
"""
caching audit services module.
"""

from pyrin.application.services import get_component
from pyrin.caching.audit import CachingAuditPackage


def inspect(**options):
    """
    inspects the status of available caches.

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

    return get_component(CachingAuditPackage.COMPONENT_NAME).inspect(**options)

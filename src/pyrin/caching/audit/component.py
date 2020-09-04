# -*- coding: utf-8 -*-
"""
caching audit component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.caching.audit import CachingAuditPackage
from pyrin.caching.audit.manager import CachingAuditManager


@component(CachingAuditPackage.COMPONENT_NAME)
class CachingAuditComponent(Component, CachingAuditManager):
    """
    caching audit component class.
    """
    pass

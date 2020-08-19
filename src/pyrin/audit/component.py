# -*- coding: utf-8 -*-
"""
audit component module.
"""

from pyrin.audit import AuditPackage
from pyrin.audit.manager import AuditManager
from pyrin.application.structs import Component
from pyrin.application.decorators import component


@component(AuditPackage.COMPONENT_NAME)
class AuditComponent(Component, AuditManager):
    """
    audit component class.
    """
    pass

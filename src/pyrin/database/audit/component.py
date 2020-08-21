# -*- coding: utf-8 -*-
"""
database audit component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.database.audit import DatabaseAuditPackage
from pyrin.database.audit.manager import DatabaseAuditManager


@component(DatabaseAuditPackage.COMPONENT_NAME)
class DatabaseAuditComponent(Component, DatabaseAuditManager):
    """
    database audit component class.
    """
    pass

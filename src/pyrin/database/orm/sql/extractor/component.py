# -*- coding: utf-8 -*-
"""
orm sql extractor component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.database.orm.sql.extractor import ORMSQLExtractorPackage
from pyrin.database.orm.sql.extractor.manager import ORMSQLExtractorManager


@component(ORMSQLExtractorPackage.COMPONENT_NAME)
class ORMSQLExtractorComponent(Component, ORMSQLExtractorManager):
    """
    orm sql extractor component class.
    """
    pass

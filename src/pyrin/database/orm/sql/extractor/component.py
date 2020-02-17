# -*- coding: utf-8 -*-
"""
database orm sql extractor component module.
"""

from pyrin.application.decorators import component
from pyrin.application.context import Component
from pyrin.database.orm.sql.extractor import DatabaseORMSQLExtractorPackage
from pyrin.database.orm.sql.extractor.manager import DatabaseORMSQLExtractorManager


@component(DatabaseORMSQLExtractorPackage.COMPONENT_NAME)
class DatabaseORMSQLExtractorComponent(Component, DatabaseORMSQLExtractorManager):
    """
    database orm sql extractor component class.
    """
    pass

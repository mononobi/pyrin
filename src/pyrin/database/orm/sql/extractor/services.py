# -*- coding: utf-8 -*-
"""
orm sql extractor services module.
"""

from pyrin.application.services import get_component
from pyrin.database.orm.sql.extractor import ORMSQLExtractorPackage


def find_table_names(expression, **options):
    """
    finds table names from a string or `TextClause` sql expression.

    :param str | TextClause expression: a string or `TextClause`
                                        containing a sql expression.

    :keyword bool include_select: specifies that select statements
                                  must be investigated for table names.
                                  defaults to True if not provided.

    :keyword bool include_insert: specifies that insert statements
                                  must be investigated for table names.
                                  defaults to True if not provided.

    :keyword bool include_update: specifies that update statements
                                  must be investigated for table names.
                                  defaults to True if not provided.

    :keyword bool include_delete: specifies that delete statements
                                  must be investigated for table names.
                                  defaults to True if not provided.

    :rtype: list[str]
    """

    return get_component(ORMSQLExtractorPackage.COMPONENT_NAME).find_table_names(expression,
                                                                                 **options)

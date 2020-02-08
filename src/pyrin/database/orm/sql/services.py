# -*- coding: utf-8 -*-
"""
database orm sql services module.
"""

from pyrin.application.services import get_component
from pyrin.database.orm.sql import DatabaseORMSQLPackage


def find_table_names(expression):
    """
    finds table names from a string or `TextClause` sql expression.

    :param Union[str, TextClause] expression: a string or `TextClause`
                                              containing a sql expression.

    :returns: list[str]
    :rtype: list
    """

    return get_component(DatabaseORMSQLPackage.COMPONENT_NAME).find_table_names(expression)

# -*- coding: utf-8 -*-
"""
utils database module.
"""

from pyrin.core.exceptions import CoreValueError


def get_schema_name(database_name, schema_name):
    """
    gets fully qualified schema name for given database and schema.

    :param str database_name: database name.
    :param str schema_name: schema name.

    :raises CoreValueError: core value error.

    :returns: fully qualified schema name in the form of:
              `database_name.schema_name`

    :rtype: str
    """

    if database_name is None:
        database_name = ''

    if schema_name is None:
        schema_name = ''

    if database_name.strip() == '':
        raise CoreValueError('Database name could not be blank.')

    if schema_name.strip() == '':
        raise CoreValueError('Schema name could not be blank.')

    qualified_schema_name = '{database}.{schema}'.format(database=database_name,
                                                         schema=schema_name)

    return qualified_schema_name

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


def get_column_name(database_name, schema_name, table_name, column_name):
    """
    gets fully qualified column name for given
    database and schema and table and column.

    :param str database_name: database name.
    :param str schema_name: schema name.
    :param str table_name: table name.
    :param str column_name: column name.

    :raises CoreValueError: core value error.

    :returns: fully qualified column name in the form of:
              `database_name.schema_name.table_name.column_name`

    :rtype: str
    """

    qualified_schema = get_schema_name(database_name, schema_name)

    if table_name is None:
        table_name = ''

    if column_name is None:
        column_name = ''

    if table_name.strip() == '':
        raise CoreValueError('Table name could not be blank.')

    if column_name.strip() == '':
        raise CoreValueError('Column name could not be blank.')

    qualified_column_name = '{schema}.{table}.{column}'.format(schema=qualified_schema,
                                                               table=table_name,
                                                               column=column_name)

    return qualified_column_name

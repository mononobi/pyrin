# -*- coding: utf-8 -*-
"""
utils database module.
"""

from pyrin.utils.exceptions import InvalidSchemaNameError, InvalidTableNameError, \
    InvalidColumnNameError


def get_schema_name(schema_name, database_name=None):
    """
    gets fully qualified schema name for given database and schema.

    if database name is not provided, it returns the schema name only.

    note that for database backends which does not support cross
    database references, you should leave `database_name=None`.

    :param str schema_name: schema name.

    :param str database_name: database name.
                              if not provided, database name
                              will be excluded from result string.

    :raises InvalidSchemaNameError: invalid schema name error.

    :returns: fully qualified schema name in the form of:
              `database_name.schema_name` or `schema_name`

    :rtype: str
    """

    if database_name is None:
        database_name = ''

    if schema_name is None:
        schema_name = ''

    database_name = database_name.strip()
    schema_name = schema_name.strip()

    if schema_name == '':
        raise InvalidSchemaNameError('Schema name could not be blank.')

    if database_name == '':
        return schema_name

    return '{database}.{schema}'.format(database=database_name, schema=schema_name)


def get_column_name(schema_name, table_name, column_name, database_name=None):
    """
    gets fully qualified column name for given database and schema and table and column.

    note that for database backends which does not support cross
    database references, you should leave `database_name=None`.

    :param str schema_name: schema name.
    :param str table_name: table name.
    :param str column_name: column name.

    :param str database_name: database name.
                              if not provided, database name
                              will be excluded from result string.

    :raises InvalidTableNameError: invalid table name error.
    :raises InvalidColumnNameError: invalid column name error.

    :returns: fully qualified column name in the form of:
              `database_name.schema_name.table_name.column_name` or
              `schema_name.table_name.column_name`

    :rtype: str
    """

    qualified_schema = get_schema_name(schema_name, database_name)

    if table_name is None:
        table_name = ''

    if column_name is None:
        column_name = ''

    table_name = table_name.strip()
    column_name = column_name.strip()

    if table_name == '':
        raise InvalidTableNameError('Table name could not be blank.')

    if column_name == '':
        raise InvalidColumnNameError('Column name could not be blank.')

    return '{schema}.{table}.{column}'.format(schema=qualified_schema,
                                              table=table_name,
                                              column=column_name)

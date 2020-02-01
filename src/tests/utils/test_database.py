# -*- coding: utf-8 -*-
"""
utils test_database module.
"""

import pytest

import pyrin.utils.database as database_utils

from pyrin.utils.exceptions import InvalidSchemaNameError, InvalidTableNameError, \
    InvalidColumnNameError


def test_get_schema_name():
    """
    gets fully qualified schema name for given database and schema.
    """

    schema_name = database_utils.get_schema_name('schema', 'database')

    assert schema_name == 'database.schema'


def test_get_schema_name_without_database():
    """
    gets fully qualified schema name without specifying database name.
    """

    schema_name1 = database_utils.get_schema_name('schema')
    schema_name2 = database_utils.get_schema_name('schema', None)
    schema_name3 = database_utils.get_schema_name('schema', '')
    schema_name4 = database_utils.get_schema_name('schema', '  ')

    assert schema_name1 == 'schema'
    assert schema_name2 == 'schema'
    assert schema_name3 == 'schema'
    assert schema_name4 == 'schema'


def test_get_schema_name_with_invalid_schema():
    """
    gets fully qualified schema name for given database and invalid schema.
    it should raise an error.
    """

    with pytest.raises(InvalidSchemaNameError):
        database_utils.get_schema_name('  ', 'database')


def test_get_column_name():
    """
    gets fully qualified column name for given
    database and schema and table and column.
    """

    column_name = database_utils.get_column_name('schema', 'table', 'column', 'database')

    assert column_name == 'database.schema.table.column'


def test_get_column_name_without_database():
    """
    gets fully qualified column name for given schema
    and table and column without specifying database name.
    """

    column_name1 = database_utils.get_column_name('schema', 'table', 'column')
    column_name2 = database_utils.get_column_name('schema', 'table', 'column', None)
    column_name3 = database_utils.get_column_name('schema', 'table', 'column', '')
    column_name4 = database_utils.get_column_name('schema', 'table', 'column', '  ')

    assert column_name1 == 'schema.table.column'
    assert column_name2 == 'schema.table.column'
    assert column_name3 == 'schema.table.column'
    assert column_name4 == 'schema.table.column'


def test_get_column_name_with_invalid_schema():
    """
    gets fully qualified column name for given database
    and invalid schema and table and column.
    it should raise an error.
    """

    with pytest.raises(InvalidSchemaNameError):
        database_utils.get_column_name('  ', 'table', 'column', 'database')


def test_get_column_name_with_invalid_table():
    """
    gets fully qualified column name for given database
    and schema and invalid table and column.
    it should raise an error.
    """

    with pytest.raises(InvalidTableNameError):
        database_utils.get_column_name('schema', None, 'column', 'database')


def test_get_column_name_with_invalid_column():
    """
    gets fully qualified column name for given database
    and schema and table and invalid column.
    it should raise an error.
    """

    with pytest.raises(InvalidColumnNameError):
        database_utils.get_column_name('schema', 'table', '', 'database')

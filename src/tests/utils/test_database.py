# -*- coding: utf-8 -*-
"""
utils test_database module.
"""

import pytest

import pyrin.utils.database as database_utils

from pyrin.core.exceptions import CoreValueError


def test_get_schema_name():
    """
    gets fully qualified schema name for given database and schema.
    """

    schema_name = database_utils.get_schema_name('database', 'schema')

    assert schema_name == 'database.schema'


def test_get_schema_name_with_invalid_database():
    """
    gets fully qualified schema name for given invalid database and schema.
    it should raise an error.
    """

    with pytest.raises(CoreValueError):
        database_utils.get_schema_name(None, 'schema')


def test_get_schema_name_with_invalid_schema():
    """
    gets fully qualified schema name for given database and invalid schema.
    it should raise an error.
    """

    with pytest.raises(CoreValueError):
        database_utils.get_schema_name('database', '  ')


def test_get_column_name():
    """
    gets fully qualified column name for given
    database and schema and table and column.
    """

    column_name = database_utils.get_column_name('database', 'schema', 'table', 'column')

    assert column_name == 'database.schema.table.column'


def test_get_column_name_with_invalid_database():
    """
    gets fully qualified column name for given invalid
    database and schema and table and column.
    it should raise an error.
    """

    with pytest.raises(CoreValueError):
        database_utils.get_column_name(None, 'schema', 'table', 'column')


def test_get_column_name_with_invalid_schema():
    """
    gets fully qualified column name for given database
    and invalid schema and table and column.
    it should raise an error.
    """

    with pytest.raises(CoreValueError):
        database_utils.get_column_name('database', '  ', 'table', 'column')


def test_get_column_name_with_invalid_table():
    """
    gets fully qualified column name for given database
    and schema and invalid table and column.
    it should raise an error.
    """

    with pytest.raises(CoreValueError):
        database_utils.get_column_name('database', 'schema', None, 'column')


def test_get_column_name_with_invalid_column():
    """
    gets fully qualified column name for given database
    and schema and table and invalid column.
    it should raise an error.
    """

    with pytest.raises(CoreValueError):
        database_utils.get_column_name('database', 'schema', 'table', '')

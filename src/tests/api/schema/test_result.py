# -*- coding: utf-8 -*-
"""
schema test_result module.
"""

import pytest

from pyrin.api.schema.exceptions import SchemaAttributesRequiredError
from pyrin.api.schema.result import ResultSchema
from pyrin.converters.serializer.handlers.exceptions import ColumnNotExistedError

from tests.common.generator import generate_row_results


def test_create_schema():
    """
    creates a result schema.
    """

    columns = ['id', 'name']
    exclude = ['age']
    rename = dict(name='new_name')
    exposed_only = False
    depth = 2

    schema = ResultSchema(columns=columns,
                          exclude=exclude,
                          rename=rename,
                          exposed_only=exposed_only,
                          depth=depth)

    assert schema.columns == columns
    assert schema.exclude == exclude
    assert schema.rename == rename
    assert schema.exposed_only is exposed_only
    assert schema.depth == depth


def test_create_schema_with_some_input():
    """
    creates a result schema by providing some of inputs.
    """

    columns = ['id', 'name']

    schema = ResultSchema(columns=columns, depth=3)

    assert schema.columns == columns
    assert schema.exclude is None
    assert schema.rename is None
    assert schema.exposed_only is None
    assert schema.depth == 3


def test_create_schema_without_input():
    """
    creates a result schema without providing any inputs.
    it should raise an error.
    """

    with(pytest.raises(SchemaAttributesRequiredError)):
        schema = ResultSchema()


def test_create_schema_with_none_input():
    """
    creates a result schema by providing None inputs.
    it should raise an error.
    """

    with(pytest.raises(SchemaAttributesRequiredError)):
        schema = ResultSchema(depth=None)


def test_create_schema_with_empty_input():
    """
    creates a result schema by providing empty inputs.
    it should raise an error.
    """

    with(pytest.raises(SchemaAttributesRequiredError)):
        schema = ResultSchema(columns=dict())


def test_filter_single_row():
    """
    filters single row result using given schema.
    """

    columns = ['id', 'name', 'age', 'extra']
    exclude = ['name', 'unavailable']
    rename = dict(id='new_id', age='new_age')

    schema = ResultSchema(columns=columns,
                          exclude=exclude,
                          rename=rename)

    results = generate_row_results(1,
                                   ['id', 'name', 'extra', 'age'],
                                   [1, 'some_name', 'some_extra', 20])

    filtered = schema.filter(results[0])

    assert filtered is not results[0]
    assert isinstance(filtered, dict)
    assert sorted(list(filtered.keys())) == sorted(['extra', 'new_id', 'new_age'])


def test_filter_rows_with_columns():
    """
    filters row results using given schema which has columns attribute.
    """

    columns = ['id', 'name']
    schema = ResultSchema(columns=columns)

    results = generate_row_results(20,
                                   ['id', 'name', 'extra', 'age'],
                                   [1, 'some_name', 'some_extra', 20])

    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 2 for item in filtered)
    assert all(sorted(list(item.keys())) == sorted(['id', 'name']) for item in filtered)


def test_filter_rows_with_exclude():
    """
    filters row results using given schema which has exclude attribute.
    """

    exclude = ['id', 'name', 'fake']
    schema = ResultSchema(exclude=exclude)

    results = generate_row_results(20,
                                   ['id', 'name', 'extra', 'age'],
                                   [1, 'some_name', 'some_extra', 20])

    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 2 for item in filtered)
    assert all(sorted(list(item.keys())) == sorted(['extra', 'age']) for item in filtered)


def test_filter_rows_with_rename():
    """
    filters row results using given schema which has rename attribute.
    """

    rename = dict(id='new_id', extra='new_extra',
                  age='new_age', name='name', fake='fake')

    schema = ResultSchema(rename=rename)

    results = generate_row_results(20,
                                   ['id', 'name', 'extra', 'age'],
                                   [1, 'some_name', 'some_extra', 20])

    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 4 for item in filtered)
    assert all(sorted(list(item.keys())) ==
               sorted(['new_id', 'new_extra', 'new_age', 'name']) for item in filtered)


def test_filter_rows_with_columns_rename():
    """
    filters row results using given schema which has columns and rename attributes.
    """

    columns = ['id', 'name']
    rename = dict(name='new_name')

    schema = ResultSchema(columns=columns,
                          rename=rename,
                          exposed_only=False)

    results = generate_row_results(20,
                                   ['id', 'name', 'extra', 'age'],
                                   [1, 'some_name', 'some_extra', 20])

    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 2 for item in filtered)
    assert all(sorted(list(item.keys())) == sorted(['id', 'new_name']) for item in filtered)


def test_filter_rows_with_exclude_rename():
    """
    filters row results using given schema which has exclude and rename attributes.
    """

    exclude = ['id', 'name']
    rename = dict(car='new_car', id='new_id')

    schema = ResultSchema(exclude=exclude,
                          rename=rename,
                          depth=4)

    results = generate_row_results(20,
                                   ['id', 'name', 'extra', 'car'],
                                   [1, 'some_name', 'some_extra', 'some_car'])

    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 2 for item in filtered)
    assert all(sorted(list(item.keys())) == sorted(['extra', 'new_car']) for item in filtered)


def test_filter_rows_with_columns_exclude():
    """
    filters row results using given schema which has columns and exclude attributes.
    """

    columns = ['id', 'name', 'age']
    exclude = ['name']

    schema = ResultSchema(columns=columns,
                          exclude=exclude)

    results = generate_row_results(20,
                                   ['id', 'name', 'extra', 'age'],
                                   [1, 'some_name', 'some_extra', 20])

    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 2 for item in filtered)
    assert all(sorted(list(item.keys())) == sorted(['id', 'age']) for item in filtered)


def test_filter_rows_with_columns_exclude_rename():
    """
    filters row results using given schema which has
    columns and exclude and rename attributes.
    """

    columns = ['id', 'name', 'age', 'extra']
    exclude = ['name', 'unavailable']
    rename = dict(id='new_id', age='new_age')

    schema = ResultSchema(columns=columns,
                          exclude=exclude,
                          rename=rename)

    results = generate_row_results(20,
                                   ['id', 'name', 'extra', 'age'],
                                   [1, 'some_name', 'some_extra', 20])

    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 3 for item in filtered)
    assert all(sorted(list(item.keys())) ==
               sorted(['extra', 'new_id', 'new_age']) for item in filtered)


def test_filter_rows_with_invalid_columns():
    """
    filters row results using given schema which has
    invalid columns attribute. it should raise an error.
    """

    columns = ['id', 'name', 'age', 'extra', 'fake_column', 'not_available']
    schema = ResultSchema(columns=columns)

    results = generate_row_results(20,
                                   ['id', 'name', 'extra', 'age'],
                                   [1, 'some_name', 'some_extra', 20])

    with pytest.raises(ColumnNotExistedError):
        filtered = schema.filter(results)


def test_filter_rows_with_columns_and_invalid_exclude_rename():
    """
    filters row results using given schema which has
    columns attribute and invalid exclude and rename attributes.
    """

    columns = ['id', 'name']
    exclude = ['name', 'unavailable', 'fake']
    rename = dict(id='new_id', fake='new_fake', not_present='not_present')

    schema = ResultSchema(columns=columns,
                          exclude=exclude,
                          rename=rename)

    results = generate_row_results(20,
                                   ['id', 'name', 'extra', 'age'],
                                   [1, 'some_name', 'some_extra', 20])

    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 1 for item in filtered)
    assert all(sorted(list(item.keys())) ==
               sorted(['new_id']) for item in filtered)


def test_filter_not_valid_items():
    """
    filters the item which is not valid. it should return the same input value.
    """

    schema = ResultSchema(depth=5)
    results = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is results
    assert all(isinstance(item, tuple) for item in filtered)


def test_filter_none_item():
    """
    filters the item which is None. it should return the same input value.
    """

    schema = ResultSchema(exposed_only=True)
    filtered = schema.filter(None)

    assert filtered is None

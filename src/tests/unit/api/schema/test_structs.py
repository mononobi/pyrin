# -*- coding: utf-8 -*-
"""
schema test_structs module.
"""

import pytest

from pyrin.api.schema.structs import ResultSchema
from pyrin.core.globals import SECURE_FALSE, SECURE_TRUE
from pyrin.database.model.exceptions import InvalidDepthProvidedError

from tests.unit.common.generator import generate_row_results, generate_entity_results
from tests.unit.common.models import RightChildEntity, SampleWithHiddenFieldEntity, \
    ChildEntity, ParentEntity


def test_create_schema():
    """
    creates a result schema.
    """

    columns = ['id', 'name']
    exclude = ['age']
    rename = dict(name='new_name')
    exposed_only = SECURE_FALSE
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


def test_filter_single_row():
    """
    filters single row result using given schema.
    """

    columns = ['id', 'name', 'age', 'extra']
    exclude = ['name', 'unavailable']
    rename = dict(id='new_id', age='new_age')
    schema = ResultSchema(columns=columns, exclude=exclude, rename=rename)

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
    schema = ResultSchema(columns=columns, rename=rename, exposed_only=SECURE_FALSE)

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
    schema = ResultSchema(exclude=exclude, rename=rename, depth=4)

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
    schema = ResultSchema(columns=columns, exclude=exclude)

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
    schema = ResultSchema(columns=columns, exclude=exclude, rename=rename)

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
    invalid columns attribute. it should not raise an error.
    """

    columns = ['id', 'name', 'age', 'extra', 'fake_column', 'not_available']
    schema = ResultSchema(columns=columns)

    results = generate_row_results(20,
                                   ['id', 'name', 'extra', 'age'],
                                   [1, 'some_name', 'some_extra', 20])

    schema.filter(results)


def test_filter_rows_with_columns_and_invalid_exclude_rename():
    """
    filters row results using given schema which has
    columns attribute and invalid exclude and rename attributes.
    """

    columns = ['id', 'name']
    exclude = ['name', 'unavailable', 'fake']
    rename = dict(id='new_id', fake='new_fake', not_present='not_present')

    schema = ResultSchema(columns=columns, exclude=exclude, rename=rename)

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


def test_filter_invalid_items():
    """
    filters the item which is not valid. it should return a list equal to input list.
    """

    schema = ResultSchema(depth=5)
    results = [{1, 2, 3}, {4, 5, 6}, {7, 8, 9}]
    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered == results
    assert all(isinstance(item, set) for item in filtered)


def test_filter_none_item():
    """
    filters the item which is None. it should return the same input value.
    """

    schema = ResultSchema(exposed_only=SECURE_TRUE)
    filtered = schema.filter(None)

    assert filtered is None


def test_filter_single_entity():
    """
    filters single entity result using given schema.
    """

    columns = ['id', 'age']
    exclude = ['id', 'unavailable']
    rename = dict(id='new_id', age='new_age')
    schema = ResultSchema(columns=columns, exclude=exclude, rename=rename)

    kwargs = dict(id=1, age=25, grade=5)
    results = generate_entity_results(RightChildEntity, 1, **kwargs, populate_all=SECURE_TRUE)
    filtered = schema.filter(results[0])

    assert filtered is not results[0]
    assert isinstance(filtered, dict)
    assert sorted(list(filtered.keys())) == sorted(['new_age'])


def test_filter_entities_with_columns():
    """
    filters entity results using given schema which has columns attribute.
    """

    columns = ['id', 'age']
    schema = ResultSchema(columns=columns)

    kwargs = dict(id=1, age=25, grade=5)
    results = generate_entity_results(RightChildEntity, 20, **kwargs, populate_all=SECURE_TRUE)
    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 2 for item in filtered)
    assert all(sorted(list(item.keys())) == sorted(['id', 'age']) for item in filtered)


def test_filter_entities_with_exclude():
    """
    filters entity results using given schema which has exclude attribute.
    """

    exclude = ['id', 'age', 'fake']
    schema = ResultSchema(exclude=exclude)

    kwargs = dict(id=1, age=25, grade=5)
    results = generate_entity_results(RightChildEntity, 20, **kwargs, populate_all=SECURE_TRUE)
    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 1 for item in filtered)
    assert all(sorted(list(item.keys())) == sorted(['grade']) for item in filtered)


def test_filter_entities_with_rename():
    """
    filters entity results using given schema which has rename attribute.
    """

    rename = dict(id='new_id', extra='new_extra',
                  age='new_age', name='name', fake='fake')

    schema = ResultSchema(rename=rename)

    kwargs = dict(id=1, age=25, grade=5)
    results = generate_entity_results(RightChildEntity, 20, **kwargs, populate_all=SECURE_TRUE)
    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 3 for item in filtered)
    assert all(sorted(list(item.keys())) ==
               sorted(['new_id', 'new_age', 'grade']) for item in filtered)


def test_filter_entities_with_columns_rename():
    """
    filters entity results using given schema which has columns and rename attributes.
    """

    columns = ['id', 'grade']
    rename = dict(grade='new_grade')
    schema = ResultSchema(columns=columns, rename=rename, exposed_only=SECURE_FALSE)

    kwargs = dict(id=1, age=25, grade=5)
    results = generate_entity_results(RightChildEntity, 20, **kwargs,
                                      populate_all=SECURE_TRUE)
    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 2 for item in filtered)
    assert all(sorted(list(item.keys())) == sorted(['id', 'new_grade']) for item in filtered)


def test_filter_entities_with_exclude_rename():
    """
    filters entity results using given schema which has exclude and rename attributes.
    """

    exclude = ['id']
    rename = dict(grade='new_grade', id='new_id')
    schema = ResultSchema(exclude=exclude, rename=rename, depth=4)

    kwargs = dict(id=1, age=25, grade=5)
    results = generate_entity_results(RightChildEntity, 20, **kwargs, populate_all=SECURE_TRUE)
    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 2 for item in filtered)
    assert all(sorted(list(item.keys())) == sorted(['age', 'new_grade']) for item in filtered)


def test_filter_entities_with_columns_exclude():
    """
    filters entity results using given schema which has columns and exclude attributes.
    """

    columns = ['id', 'grade', 'age']
    exclude = ['grade']
    schema = ResultSchema(columns=columns, exclude=exclude)

    kwargs = dict(id=1, age=25, grade=5)
    results = generate_entity_results(RightChildEntity, 20, **kwargs, populate_all=SECURE_TRUE)
    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 2 for item in filtered)
    assert all(sorted(list(item.keys())) == sorted(['id', 'age']) for item in filtered)


def test_filter_entities_with_columns_exclude_rename():
    """
    filters entity results using given schema which has
    columns and exclude and rename attributes.
    """

    columns = ['id', 'grade', 'age']
    exclude = ['age', 'unavailable']
    rename = dict(id='new_id', age='new_age')
    schema = ResultSchema(columns=columns, exclude=exclude, rename=rename)

    kwargs = dict(id=1, age=25, grade=5)
    results = generate_entity_results(RightChildEntity, 20, **kwargs, populate_all=SECURE_TRUE)
    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 2 for item in filtered)
    assert all(sorted(list(item.keys())) ==
               sorted(['new_id', 'grade']) for item in filtered)


def test_filter_entities_with_invalid_columns():
    """
    filters entity results using given schema which has
    invalid columns attribute. it should not raise an error.
    """

    columns = ['id', 'name', 'age', 'extra', 'fake_column', 'not_available']
    schema = ResultSchema(columns=columns)
    kwargs = dict(id=1, age=25, grade=5)
    results = generate_entity_results(RightChildEntity, 20, **kwargs, populate_all=SECURE_TRUE)
    schema.filter(results)


def test_filter_entities_with_columns_and_invalid_exclude_rename():
    """
    filters entity results using given schema which has
    columns attribute and invalid exclude and rename attributes.
    """

    columns = ['id', 'age']
    exclude = ['name', 'unavailable', 'fake']
    rename = dict(id='new_id', fake='new_fake', not_present='not_present')
    schema = ResultSchema(columns=columns, exclude=exclude, rename=rename)

    kwargs = dict(id=1, age=25, grade=5)
    results = generate_entity_results(RightChildEntity, 20, **kwargs, populate_all=SECURE_TRUE)
    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 2 for item in filtered)
    assert all(sorted(list(item.keys())) ==
               sorted(['new_id', 'age']) for item in filtered)


def test_filter_entities_with_exposed_only_true():
    """
    filters entity results using given schema which have `exposed_only=SECURE_TRUE` attribute.
    """

    rename = dict(id='new_id', fake='new_fake', not_present='not_present')
    schema = ResultSchema(rename=rename)

    kwargs = dict(id=1, sub_id='sub_1', age=25, name='some_name', hidden_field='some_secret')
    results = generate_entity_results(SampleWithHiddenFieldEntity, 20,
                                      **kwargs, populate_all=SECURE_TRUE)
    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 4 for item in filtered)
    assert all(sorted(list(item.keys())) ==
               sorted(['new_id', 'sub_id', 'age', 'name']) for item in filtered)


def test_filter_entities_with_exposed_only_false():
    """
    filters entity results using given schema which have `exposed_only=SECURE_FALSE` attribute.
    """

    rename = dict(id='new_id', fake='new_fake', not_present='not_present')
    schema = ResultSchema(rename=rename, exposed_only=SECURE_FALSE)

    kwargs = dict(id=1, sub_id='sub_1', age=25, name='some_name', hidden_field='some_secret')
    results = generate_entity_results(SampleWithHiddenFieldEntity, 20,
                                      **kwargs, populate_all=SECURE_TRUE)
    filtered = schema.filter(results)

    assert len(filtered) == len(results)
    assert filtered is not results
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 5 for item in filtered)
    assert all(sorted(list(item.keys())) ==
               sorted(['new_id', 'sub_id', 'age', 'name', 'hidden_field']) for item in filtered)


def test_filter_related_entities_without_depth():
    """
    filters entity results which have relationships
    using given schema with `depth=0` attribute.
    """

    schema = ResultSchema(depth=0)
    child_kwargs = dict(name='child_name', parent=ParentEntity(name='parent_name'))
    children = generate_entity_results(ChildEntity, 20, **child_kwargs, populate_all=SECURE_TRUE)
    filtered = schema.filter(children)

    assert len(filtered) == len(children)
    assert filtered is not children
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 3 for item in filtered)
    assert all(sorted(list(item.keys())) ==
               sorted(['id', 'name', 'parent_id']) for item in filtered)


def test_filter_related_entities_with_depth():
    """
    filters entity results which have relationships
    using given schema with `depth=1` attribute.
    """

    schema = ResultSchema(depth=1)
    child_kwargs = dict(name='child_name', parent=ParentEntity(name='parent_name'))
    children = generate_entity_results(ChildEntity, 20, **child_kwargs, populate_all=SECURE_TRUE)
    filtered = schema.filter(children)

    assert len(filtered) == len(children)
    assert filtered is not children
    assert all(isinstance(item, dict) for item in filtered)
    assert all(len(item) == 4 for item in filtered)
    assert all(sorted(list(item.keys())) ==
               sorted(['id', 'name', 'parent_id', 'parent']) for item in filtered)
    assert all(isinstance(item.get('parent'), dict) for item in filtered)
    assert all(sorted(list(item.get('parent').keys())) ==
               sorted(['id', 'name']) for item in filtered)


def test_filter_related_entities_with_invalid_depth():
    """
    filters entity results which have relationships using given schema
    with invalid depth attribute. it should raise an error.
    """

    schema = ResultSchema(depth=6)
    child_kwargs = dict(name='child_name', parent=ParentEntity(name='parent_name'))
    children = generate_entity_results(ChildEntity, 20, **child_kwargs, populate_all=SECURE_TRUE)

    with pytest.raises(InvalidDepthProvidedError):
        filtered = schema.filter(children)

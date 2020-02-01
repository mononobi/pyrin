# -*- coding: utf-8 -*-
"""
utils test_sqlalchemy module.
"""

import pytest

import pyrin.utils.sqlalchemy as sqlalchemy_utils

from pyrin.core.context import DTO
from pyrin.utils.exceptions import FieldsAndValuesCountMismatchError, \
    InvalidRowResultFieldsAndValuesError

from tests.common.models import SampleEntity, SampleWithHiddenFieldEntity


def test_entity_to_dict():
    """
    converts the given entity into a dict and returns it.
    """

    id = 1000
    name = 'no name'
    age = 32

    entity = SampleEntity()
    entity.id = id
    entity.name = name
    entity.age = age

    result = sqlalchemy_utils.entity_to_dict(entity)

    assert isinstance(result, dict) is True
    assert len(result) == 3
    assert result['id'] == id
    assert result['name'] == name
    assert result['age'] == age


def test_entity_to_dict_with_none_entity():
    """
    converts the given entity which is none into a dict and returns it.
    it should get an empty dict.
    """

    result = sqlalchemy_utils.entity_to_dict(None)

    assert isinstance(result, dict) is True
    assert len(result) == 0


def test_entity_to_dict_with_hidden_column():
    """
    converts the given entity into a dict and returns it.
    the entity has a hidden column which should not be
    present in result dict.
    """

    id = 1000
    sub_id = 'sub_1000'
    name = 'no name'
    age = 32
    hidden_field = 'I am hidden.'

    entity = SampleWithHiddenFieldEntity()
    entity.id = id
    entity.sub_id = sub_id
    entity.name = name
    entity.age = age
    entity.hidden_field = hidden_field

    result = sqlalchemy_utils.entity_to_dict(entity)

    assert isinstance(result, dict) is True
    assert len(result) == 4
    assert result['id'] == id
    assert result['sub_id'] == sub_id
    assert result['name'] == name
    assert result['age'] == age
    assert 'hidden_field' not in result


def test_dict_to_entity():
    """
    converts the given dict into an specified entity and returns it.
    """

    id = 1300
    name = 'jack'
    age = 40

    dict_value = DTO(id=id, name=name, age=age, ignored_key='nothing')
    entity = sqlalchemy_utils.dict_to_entity(SampleEntity, **dict_value)

    assert entity is not None
    assert entity.id == id
    assert entity.name == name
    assert entity.age == age
    assert hasattr(entity, 'ignored_key') is False


def test_dict_to_entity_with_none_dict():
    """
    converts the given dict which is none into an specified entity and returns it.
    it should get an entity with default values.
    """

    entity = sqlalchemy_utils.dict_to_entity(SampleEntity)

    assert entity is not None
    assert entity.id is None
    assert entity.name is None
    assert entity.age is None


def test_entity_to_dict_list():
    """
    converts the given list of entities into a list of dicts.
    """

    entity1 = SampleEntity()
    entity1.id = 1000
    entity1.name = 'name1'
    entity1.age = 10

    entity2 = SampleEntity()
    entity2.id = 2000
    entity2.name = 'name2'
    entity2.age = 20

    entity3 = SampleEntity()
    entity3.id = 3000
    entity3.name = 'name3'
    entity3.age = 30

    entities = [entity1, entity2, entity3]

    result = sqlalchemy_utils.entity_to_dict_list(entities)

    assert isinstance(result, list)
    assert len(result) == 3

    dict1 = result[0]
    dict2 = result[1]
    dict3 = result[2]

    assert isinstance(dict1, dict)
    assert isinstance(dict2, dict)
    assert isinstance(dict3, dict)

    assert dict1.get('id', None) == 1000
    assert dict2.get('id', None) == 2000
    assert dict3.get('id', None) == 3000

    assert dict1.get('name', None) == 'name1'
    assert dict2.get('name', None) == 'name2'
    assert dict3.get('name', None) == 'name3'

    assert dict1.get('age', None) == 10
    assert dict2.get('age', None) == 20
    assert dict3.get('age', None) == 30


def test_entity_to_dict_list_with_single_item():
    """
    converts the given list of single entity into a list of a single dict.
    """

    entity1 = SampleEntity()
    entity1.id = 1000
    entity1.name = 'name1'
    entity1.age = 10

    entities = [entity1]

    result = sqlalchemy_utils.entity_to_dict_list(entities)

    assert isinstance(result, list)
    assert len(result) == 1

    dict1 = result[0]

    assert isinstance(dict1, dict)

    assert dict1.get('id', None) == 1000
    assert dict1.get('name', None) == 'name1'
    assert dict1.get('age', None) == 10


def test_entity_to_dict_list_with_empty_list():
    """
    converts the given empty list into a list of a dicts.
    it should return an empty list.
    """

    result = sqlalchemy_utils.entity_to_dict_list([])

    assert isinstance(result, list)
    assert len(result) == 0


def test_entity_to_dict_list_with_none():
    """
    converts the given None value into a list of a dicts.
    it should return an empty list.
    """

    result = sqlalchemy_utils.entity_to_dict_list(None)

    assert isinstance(result, list)
    assert len(result) == 0


def test_keyed_tuple_to_dict():
    """
    converts values list into a dict using given columns list.
    """

    values = ['this is name', 1000, 22]
    fields = ['name', 'id', 'age']

    row_result = sqlalchemy_utils.create_row_result(fields, values)
    result = sqlalchemy_utils.keyed_tuple_to_dict(row_result)

    assert isinstance(result, dict)
    assert len(result) == 3

    assert result.get('name', None) == 'this is name'
    assert result.get('id', None) == 1000
    assert result.get('age', None) == 22


def test_keyed_tuple_to_dict_with_none_items():
    """
    converts values list into a dict using given columns list.
    it should return an empty dict in different scenarios.
    """

    result1 = sqlalchemy_utils.keyed_tuple_to_dict(None)
    result2 = sqlalchemy_utils.keyed_tuple_to_dict([])

    assert isinstance(result1, dict)
    assert isinstance(result2, dict)

    assert len(result1) == 0
    assert len(result2) == 0


def test_keyed_tuple_to_dict_list():
    """
    converts the given list of values list into a list
    of dicts using given columns list.
    """

    columns = ['name', 'id', 'age']
    values1 = ['name1', 1000, 10]
    values2 = ['name2', 2000, 20]
    values3 = ['name3', 3000, 30]
    values = [values1, values2, values3]

    rows = []
    for single_value in values:
        row = sqlalchemy_utils.create_row_result(columns, single_value)
        rows.append(row)

    results = sqlalchemy_utils.keyed_tuple_to_dict_list(rows)

    assert isinstance(results, list)
    assert len(results) == 3

    dict1 = results[0]
    dict2 = results[1]
    dict3 = results[2]

    assert isinstance(dict1, dict)
    assert isinstance(dict2, dict)
    assert isinstance(dict3, dict)

    assert dict1.get('id', None) == 1000
    assert dict2.get('id', None) == 2000
    assert dict3.get('id', None) == 3000

    assert dict1.get('name', None) == 'name1'
    assert dict2.get('name', None) == 'name2'
    assert dict3.get('name', None) == 'name3'

    assert dict1.get('age', None) == 10
    assert dict2.get('age', None) == 20
    assert dict3.get('age', None) == 30


def test_keyed_tuple_to_dict_list_with_none_items():
    """
    converts the given list of values list into a list
    of dicts using given columns list.
    it should return an empty list or a list with empty
    dicts in different scenarios.
    """

    columns = []
    values = [[], []]

    rows = []
    for single_value in values:
        row = sqlalchemy_utils.create_row_result(columns, single_value)
        rows.append(row)

    results = sqlalchemy_utils.keyed_tuple_to_dict_list(rows)

    assert isinstance(results, list)
    assert len(results) == 2
    assert isinstance(results[0], dict)
    assert isinstance(results[1], dict)
    assert len(results[0]) == 0
    assert len(results[1]) == 0

    results2 = sqlalchemy_utils.keyed_tuple_to_dict_list([None, None])

    assert isinstance(results2, list)
    assert len(results2) == 2
    assert isinstance(results2[0], dict)
    assert isinstance(results2[1], dict)
    assert len(results2[0]) == 0
    assert len(results2[1]) == 0

    results3 = sqlalchemy_utils.keyed_tuple_to_dict_list(None)

    assert isinstance(results3, list)
    assert len(results3) == 0

    results4 = sqlalchemy_utils.keyed_tuple_to_dict_list([])

    assert isinstance(results4, list)
    assert len(results4) == 0


def test_like_both():
    """
    gets a copy of string with `%` attached to both
    ends of it to use in like operator.
    """

    value = 'sample_string'
    result = sqlalchemy_utils.like_both(value)

    assert result == '%sample_string%'


def test_like_both_with_none_value():
    """
    gets a copy of string which is None with `%` attached to both
    ends of it to use in like operator.
    """

    result = sqlalchemy_utils.like_both(None)

    assert result == '%%'


def test_like_begin():
    """
    gets a copy of string with `%` attached to beginning
    of it to use in like operator.
    """

    value = 'sample_string'
    result = sqlalchemy_utils.like_begin(value)

    assert result == '%sample_string'


def test_like_begin_with_none_value():
    """
    gets a copy of string which is None with `%` attached
    to beginning of it to use in like operator.
    """

    result = sqlalchemy_utils.like_begin(None)

    assert result == '%'


def test_like_end():
    """
    gets a copy of string with `%` attached to end
    of it to use in like operator.
    """

    value = 'sample_string'
    result = sqlalchemy_utils.like_end(value)

    assert result == 'sample_string%'


def test_like_end_with_none_value():
    """
    gets a copy of string which is None with `%` attached
    to end of it to use in like operator.
    """

    result = sqlalchemy_utils.like_end(None)

    assert result == '%'


def test_create_row_result():
    """
    creates a row result from values list and columns names.
    """

    columns = ['name', 'id', 'age']
    values = ['this is name', 1000, 22]

    result = sqlalchemy_utils.create_row_result(columns, values)

    assert result is not None
    assert result.name == 'this is name'
    assert result.id == 1000
    assert result.age == 22


def test_create_row_result_with_mismatch_length():
    """
    creates a row result from values list and columns names.
    it should raise an error because columns and values length does not match.
    """

    columns = ['name', 'id', 'age']
    values = ['this is name', 1000, 22, 'extra']

    with pytest.raises(FieldsAndValuesCountMismatchError):
        sqlalchemy_utils.create_row_result(columns, values)


def test_create_row_result_with_none_values():
    """
    creates a row result from values list and columns names.
    it should raise an error because columns and values are None.
    """

    with pytest.raises(InvalidRowResultFieldsAndValuesError):
        sqlalchemy_utils.create_row_result(None, None)

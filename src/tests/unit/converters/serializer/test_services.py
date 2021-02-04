# -*- coding: utf-8 -*-
"""
serializer test_services module.
"""

import pyrin.utils.sqlalchemy as sqlalchemy_utils
import pyrin.converters.serializer.services as serializer_services

from pyrin.core.globals import SECURE_TRUE, SECURE_FALSE

from tests.unit.common.models import RightChildEntity, SampleWithHiddenFieldEntity


def test_serialize_row_result():
    """
    serializes the given row result into dict.
    """

    row = sqlalchemy_utils.create_row_result(['id', 'name', 'age'], [1, 'jack', 20])
    result = serializer_services.serialize(row)

    assert isinstance(result, dict)
    assert len(result) == 3
    assert result.get('name', None) == 'jack'
    assert result.get('id', None) == 1
    assert result.get('age', None) == 20


def test_serialize_row_result_list():
    """
    serializes the given row result list into dict list.
    """

    row1 = sqlalchemy_utils.create_row_result(['id', 'grade', 'age'], [1, 15, 11])
    row2 = sqlalchemy_utils.create_row_result(['id', 'grade', 'age'], [2, 35, 25])
    row3 = sqlalchemy_utils.create_row_result(['id', 'grade', 'age'], [3, 45, 30])
    values = [row1, row2, row3]
    results = serializer_services.serialize(values)

    assert isinstance(results, list)
    assert len(results) == 3

    first = results[0]
    second = results[1]
    third = results[2]

    assert isinstance(first, dict)
    assert isinstance(second, dict)
    assert isinstance(third, dict)

    assert len(first) == 3
    assert len(second) == 3
    assert len(third) == 3

    assert first.get('grade', None) == 15
    assert first.get('id', None) == 1
    assert first.get('age', None) == 11
    assert second.get('grade', None) == 35
    assert second.get('id', None) == 2
    assert second.get('age', None) == 25
    assert third.get('grade', None) == 45
    assert third.get('id', None) == 3
    assert third.get('age', None) == 30


def test_serialize_row_result_list_mixed_none():
    """
    serializes the given row result list into dict list.
    the list contains some row results and some None items.
    """

    row1 = sqlalchemy_utils.create_row_result(['id', 'grade', 'age'], [1, 15, 11])
    row2 = None
    row3 = sqlalchemy_utils.create_row_result(['id', 'grade', 'age'], [3, 45, 30])
    values = [row1, row2, row3]
    results = serializer_services.serialize(values)

    assert isinstance(results, list)
    assert len(results) == 3

    first = results[0]
    second = results[1]
    third = results[2]

    assert isinstance(first, dict)
    assert second is None
    assert isinstance(third, dict)

    assert len(first) == 3
    assert len(third) == 3

    assert first.get('grade', None) == 15
    assert first.get('id', None) == 1
    assert first.get('age', None) == 11
    assert third.get('grade', None) == 45
    assert third.get('id', None) == 3
    assert third.get('age', None) == 30


def test_serialize_entity():
    """
    serializes the given entity into dict.
    """

    entity = RightChildEntity(grade=20, id=1, age=10, populate_all=SECURE_TRUE)
    result = serializer_services.serialize(entity)

    assert isinstance(result, dict)
    assert len(result) == 3
    assert result.get('grade', None) == 20
    assert result.get('id', None) == 1
    assert result.get('age', None) == 10


def test_serialize_entity_readable():
    """
    serializes the given entity into dict.
    it only serializes the readable columns.
    """

    entity = SampleWithHiddenFieldEntity(id=1, sub_id='my_sub_id', name='my_name',
                                         age=10, hidden_field='some_secret',
                                         populate_all=SECURE_TRUE)
    result = serializer_services.serialize(entity)

    assert isinstance(result, dict)
    assert len(result) == 4
    assert result.get('sub_id', None) == 'my_sub_id'
    assert result.get('id', None) == 1
    assert result.get('age', None) == 10
    assert result.get('name', None) == 'my_name'
    assert 'hidden_field' not in result


def test_serialize_entity_all():
    """
    serializes the given entity into dict.
    it serializes all columns including hidden ones.
    """

    entity = SampleWithHiddenFieldEntity(id=1, sub_id='my_sub_id', name='my_name',
                                         age=10, hidden_field='some_secret',
                                         populate_all=SECURE_TRUE)
    result = serializer_services.serialize(entity, readable=SECURE_FALSE)

    assert isinstance(result, dict)
    assert len(result) == 5
    assert result.get('sub_id', None) == 'my_sub_id'
    assert result.get('id', None) == 1
    assert result.get('age', None) == 10
    assert result.get('name', None) == 'my_name'
    assert result.get('hidden_field', None) == 'some_secret'


def test_serialize_entity_list():
    """
    serializes the given entity list into dict list.
    """

    entity1 = RightChildEntity(grade=10, id=1, age=11, populate_all=SECURE_TRUE)
    entity2 = RightChildEntity(grade=22, id=2, age=25, populate_all=SECURE_TRUE)
    entity3 = RightChildEntity(grade=32, id=3, age=30, populate_all=SECURE_TRUE)
    values = [entity1, entity2, entity3]
    results = serializer_services.serialize(values)

    assert isinstance(results, list)
    assert len(results) == 3

    first = results[0]
    second = results[1]
    third = results[2]

    assert isinstance(first, dict)
    assert isinstance(second, dict)
    assert isinstance(third, dict)

    assert len(first) == 3
    assert len(second) == 3
    assert len(third) == 3

    assert first.get('grade', None) == 10
    assert first.get('id', None) == 1
    assert first.get('age', None) == 11
    assert second.get('grade', None) == 22
    assert second.get('id', None) == 2
    assert second.get('age', None) == 25
    assert third.get('grade', None) == 32
    assert third.get('id', None) == 3
    assert third.get('age', None) == 30


def test_serialize_entity_list_readable():
    """
    serializes the given entity list into dict list.
    it only serializes readable columns.
    """

    entity1 = SampleWithHiddenFieldEntity(id=1, sub_id='1', name='my_name1',
                                          age=10, hidden_field='some_secret1',
                                          populate_all=SECURE_TRUE)
    entity2 = SampleWithHiddenFieldEntity(id=2, sub_id='2', name='my_name2',
                                          age=20, hidden_field='some_secret2',
                                          populate_all=SECURE_TRUE)
    entity3 = SampleWithHiddenFieldEntity(id=3, sub_id='3', name='my_name3',
                                          age=30, hidden_field='some_secret3',
                                          populate_all=SECURE_TRUE)
    values = [entity1, entity2, entity3]
    results = serializer_services.serialize(values)

    assert isinstance(results, list)
    assert len(results) == 3

    first = results[0]
    second = results[1]
    third = results[2]

    assert isinstance(first, dict)
    assert isinstance(second, dict)
    assert isinstance(third, dict)

    assert len(first) == 4
    assert len(second) == 4
    assert len(third) == 4

    assert first.get('sub_id', None) == '1'
    assert first.get('id', None) == 1
    assert first.get('age', None) == 10
    assert first.get('name', None) == 'my_name1'
    assert second.get('sub_id', None) == '2'
    assert second.get('id', None) == 2
    assert second.get('age', None) == 20
    assert second.get('name', None) == 'my_name2'
    assert third.get('sub_id', None) == '3'
    assert third.get('id', None) == 3
    assert third.get('age', None) == 30
    assert third.get('name', None) == 'my_name3'

    assert 'hidden_field' not in first
    assert 'hidden_field' not in second
    assert 'hidden_field' not in third


def test_serialize_entity_list_all():
    """
    serializes the given entity list into dict list.
    it serializes all columns.
    """

    entity1 = SampleWithHiddenFieldEntity(id=1, sub_id='1', name='my_name1',
                                          age=10, hidden_field='some_secret1',
                                          populate_all=SECURE_TRUE)
    entity2 = SampleWithHiddenFieldEntity(id=2, sub_id='2', name='my_name2',
                                          age=20, hidden_field='some_secret2',
                                          populate_all=SECURE_TRUE)
    entity3 = SampleWithHiddenFieldEntity(id=3, sub_id='3', name='my_name3',
                                          age=30, hidden_field='some_secret3',
                                          populate_all=SECURE_TRUE)
    values = [entity1, entity2, entity3]
    results = serializer_services.serialize(values, readable=SECURE_FALSE)

    assert isinstance(results, list)
    assert len(results) == 3

    first = results[0]
    second = results[1]
    third = results[2]

    assert isinstance(first, dict)
    assert isinstance(second, dict)
    assert isinstance(third, dict)

    assert len(first) == 5
    assert len(second) == 5
    assert len(third) == 5

    assert first.get('sub_id', None) == '1'
    assert first.get('id', None) == 1
    assert first.get('age', None) == 10
    assert first.get('name', None) == 'my_name1'
    assert first.get('hidden_field', None) == 'some_secret1'
    assert second.get('sub_id', None) == '2'
    assert second.get('id', None) == 2
    assert second.get('age', None) == 20
    assert second.get('name', None) == 'my_name2'
    assert second.get('hidden_field', None) == 'some_secret2'
    assert third.get('sub_id', None) == '3'
    assert third.get('id', None) == 3
    assert third.get('age', None) == 30
    assert third.get('name', None) == 'my_name3'
    assert third.get('hidden_field', None) == 'some_secret3'


def test_serialize_entity_list_mixed_none():
    """
    serializes the given entity list into dict list.
    the list contains some entities and some None items.
    """

    entity1 = SampleWithHiddenFieldEntity(id=1, sub_id='1', name='my_name1',
                                          age=10, hidden_field='some_secret1',
                                          populate_all=SECURE_TRUE)
    entity2 = None
    entity3 = SampleWithHiddenFieldEntity(id=3, sub_id='3', name='my_name3',
                                          age=30, hidden_field='some_secret3',
                                          populate_all=SECURE_TRUE)
    values = [entity1, entity2, entity3]
    results = serializer_services.serialize(values, readable=SECURE_TRUE)

    assert isinstance(results, list)
    assert len(results) == 3

    first = results[0]
    second = results[1]
    third = results[2]

    assert isinstance(first, dict)
    assert second is None
    assert isinstance(third, dict)

    assert len(first) == 4
    assert len(third) == 4

    assert first.get('sub_id', None) == '1'
    assert first.get('id', None) == 1
    assert first.get('age', None) == 10
    assert first.get('name', None) == 'my_name1'
    assert first.get('hidden_field', None) is None
    assert third.get('sub_id', None) == '3'
    assert third.get('id', None) == 3
    assert third.get('age', None) == 30
    assert third.get('name', None) == 'my_name3'
    assert third.get('hidden_field', None) is None


def test_serialize_none():
    """
    serializes the given None value and it should return None.
    """

    result = serializer_services.serialize(None)

    assert result is None


def test_serialize_list_empty():
    """
    serializes the given empty list and it should return an empty list.
    """

    results = serializer_services.serialize([])

    assert isinstance(results, list)
    assert len(results) == 0


def test_serialize_list_with_none_values():
    """
    serializes the given list. the list items are None.
    so it should return the same exact input list.
    """

    results = serializer_services.serialize([None, None])

    assert isinstance(results, list)
    assert len(results) == 2

    first = results[0]
    second = results[1]

    assert first is None
    assert second is None

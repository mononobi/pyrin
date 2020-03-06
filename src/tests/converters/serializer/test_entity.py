# -*- coding: utf-8 -*-
"""
serializer test_entity module.
"""

from pyrin.converters.serializer.entity import CoreEntitySerializer

from tests.common.models import RightChildEntity, SampleWithHiddenFieldEntity


def test_serialize():
    """
    serializes the given entity into dict.
    """

    entity = RightChildEntity(grade=20, id=1, age=10)
    result = CoreEntitySerializer().serialize(entity)

    assert isinstance(result, dict)
    assert len(result) == 3
    assert result.get('grade', None) == 20
    assert result.get('id', None) == 1
    assert result.get('age', None) == 10


def test_serialize_exposed_only():
    """
    serializes the given entity into dict.
    it only serializes the exposed columns.
    """

    entity = SampleWithHiddenFieldEntity(id=1, sub_id='my_sub_id', name='my_name',
                                         age=10, hidden_field='some_secret')
    result = CoreEntitySerializer().serialize(entity)

    assert isinstance(result, dict)
    assert len(result) == 4
    assert result.get('sub_id', None) == 'my_sub_id'
    assert result.get('id', None) == 1
    assert result.get('age', None) == 10
    assert result.get('name', None) == 'my_name'
    assert 'hidden_field' not in result


def test_serialize_all():
    """
    serializes the given entity into dict.
    it serializes all columns including hidden ones.
    """

    entity = SampleWithHiddenFieldEntity(id=1, sub_id='my_sub_id', name='my_name',
                                         age=10, hidden_field='some_secret')
    result = CoreEntitySerializer().serialize(entity, exposed_only=False)

    assert isinstance(result, dict)
    assert len(result) == 5
    assert result.get('sub_id', None) == 'my_sub_id'
    assert result.get('id', None) == 1
    assert result.get('age', None) == 10
    assert result.get('name', None) == 'my_name'
    assert result.get('hidden_field', None) == 'some_secret'


def test_serialize_none():
    """
    serializes the given entity into dict.
    the entity is None so it should return an empty dict.
    """

    result = CoreEntitySerializer().serialize(None)

    assert isinstance(result, dict)
    assert len(result) == 0


def test_serialize_list():
    """
    serializes the given entity list into dict list.
    """

    entity1 = RightChildEntity(grade=10, id=1, age=11)
    entity2 = RightChildEntity(grade=22, id=2, age=25)
    entity3 = RightChildEntity(grade=32, id=3, age=30)
    values = [entity1, entity2, entity3]
    results = CoreEntitySerializer().serialize_list(values)

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


def test_serialize_list_exposed_only():
    """
    serializes the given entity list into dict list.
    it only serializes exposed columns.
    """

    entity1 = SampleWithHiddenFieldEntity(id=1, sub_id='1', name='my_name1',
                                          age=10, hidden_field='some_secret1')
    entity2 = SampleWithHiddenFieldEntity(id=2, sub_id='2', name='my_name2',
                                          age=20, hidden_field='some_secret2')
    entity3 = SampleWithHiddenFieldEntity(id=3, sub_id='3', name='my_name3',
                                          age=30, hidden_field='some_secret3')
    values = [entity1, entity2, entity3]
    results = CoreEntitySerializer().serialize_list(values)

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


def test_serialize_list_all():
    """
    serializes the given entity list into dict list.
    it serializes all columns.
    """

    entity1 = SampleWithHiddenFieldEntity(id=1, sub_id='1', name='my_name1',
                                          age=10, hidden_field='some_secret1')
    entity2 = SampleWithHiddenFieldEntity(id=2, sub_id='2', name='my_name2',
                                          age=20, hidden_field='some_secret2')
    entity3 = SampleWithHiddenFieldEntity(id=3, sub_id='3', name='my_name3',
                                          age=30, hidden_field='some_secret3')
    values = [entity1, entity2, entity3]
    results = CoreEntitySerializer().serialize_list(values, exposed_only=False)

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


def test_serialize_list_none():
    """
    serializes the given entity list into dict list.
    the given list is None, so it should return an empty list.
    """

    results = CoreEntitySerializer().serialize_list(None)

    assert isinstance(results, list)
    assert len(results) == 0


def test_serialize_list_empty():
    """
    serializes the given entity list into dict list.
    the given list is empty, so it should return an empty list.
    """

    results = CoreEntitySerializer().serialize_list([])

    assert isinstance(results, list)
    assert len(results) == 0


def test_serialize_list_with_none_values():
    """
    serializes the given entity list into dict list.
    the given list contains None values, so it should
    return a list of empty dicts.
    """

    results = CoreEntitySerializer().serialize_list([None, None])

    assert isinstance(results, list)
    assert len(results) == 2

    first = results[0]
    second = results[1]

    assert isinstance(first, dict)
    assert isinstance(second, dict)
    assert len(first) == 0
    assert len(second) == 0


def test_serialize_list_mixed_none():
    """
    serializes the given entity list into dict list.
    the list contains some entities and some None items.
    """

    entity1 = SampleWithHiddenFieldEntity(id=1, sub_id='1', name='my_name1',
                                          age=10, hidden_field='some_secret1')
    entity2 = None
    entity3 = SampleWithHiddenFieldEntity(id=3, sub_id='3', name='my_name3',
                                          age=30, hidden_field='some_secret3')
    values = [entity1, entity2, entity3]
    results = CoreEntitySerializer().serialize_list(values, exposed_only=True)

    assert isinstance(results, list)
    assert len(results) == 3

    first = results[0]
    second = results[1]
    third = results[2]

    assert isinstance(first, dict)
    assert isinstance(second, dict)
    assert isinstance(third, dict)

    assert len(first) == 4
    assert len(second) == 0
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

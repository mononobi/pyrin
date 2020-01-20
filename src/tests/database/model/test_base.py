# -*- coding: utf-8 -*-
"""
model test_services module.
"""

import pytest

from pyrin.core.context import DTO
from pyrin.database.model.exceptions import ColumnNotExistedError

from tests.common.models import SampleEntity, SampleWithHiddenFieldEntity


def test_init():
    """
    initializes an entity.
    """

    entity = SampleEntity()

    assert isinstance(entity, SampleEntity)
    assert entity.id is None
    assert entity.name is None
    assert entity.age is None


def test_init_with_kwargs():
    """
    initializes an entity with keyword arguments.
    """

    entity = SampleEntity(id=1000, age=20, name='sample')

    assert isinstance(entity, SampleEntity)
    assert entity.id == 1000
    assert entity.name == 'sample'
    assert entity.age == 20


def test_init_with_invalid_kwargs():
    """
    initializes an entity with some invalid keyword arguments.
    it should raise an error.
    """

    with pytest.raises(ColumnNotExistedError):
        SampleEntity(id=1000, age=20, name='sample', invalid_kwarg=True)


def test_all_columns():
    """
    gets all column names of entity.
    """

    entity = SampleWithHiddenFieldEntity()
    fields = ['age', 'sub_id', 'id', 'name', 'hidden_field']

    assert set(fields) == set(entity.all_columns())


def test_exposed_columns():
    """
    gets exposed column names of entity.
    exposed columns are those that have `exposed=True`
    """

    entity = SampleWithHiddenFieldEntity()
    fields = ['age', 'id', 'sub_id', 'name']

    assert set(fields) == set(entity.exposed_columns())


def test_to_dict():
    """
    converts the entity into a dict and returns it.
    """

    id = 1000
    name = 'no name'
    age = 32

    entity = SampleEntity()
    entity.id = id
    entity.name = name
    entity.age = age

    result = entity.to_dict()

    assert isinstance(result, dict) is True
    assert len(result) == 3
    assert result['id'] == id
    assert result['name'] == name
    assert result['age'] == age


def test_to_dict_with_hidden_column():
    """
    converts the entity into a dict and returns it.
    the result dict only contains the exposed columns of
    the entity which are those that their `hidden` attribute
    is set to False.
    """

    id = 1000
    sub_id = 'id_1000'
    name = 'no name'
    age = 32
    hidden_field = 'I am hidden.'

    entity = SampleWithHiddenFieldEntity()
    entity.id = id
    entity.sub_id = sub_id
    entity.name = name
    entity.age = age
    entity.hidden_field = hidden_field

    result = entity.to_dict()

    assert isinstance(result, dict) is True
    assert len(result) == 4
    assert result['id'] == id
    assert result['sub_id'] == sub_id
    assert result['name'] == name
    assert result['age'] == age
    assert 'hidden_field' not in result


def test_from_dict():
    """
    updates the column values of the entity from those
    values that are available in input keyword arguments.
    """

    id = 1300
    name = 'jack'
    age = 40

    dict_value = DTO(id=id, name=name, age=age, ignored_key='nothing')
    entity = SampleEntity()
    entity.from_dict(**dict_value)

    assert entity.id == id
    assert entity.name == name
    assert entity.age == age
    assert hasattr(entity, 'ignored_key') is False


def test_from_dict_with_invalid_column_and_not_silent():
    """
    updates the column values of the entity from those
    values that are available in input keyword arguments.
    there is some invalid column names and `silent_on_invalid_column=False`
    has been set. it should raise an error.
    """

    with pytest.raises(ColumnNotExistedError):
        dict_value = DTO(id=1300, name='jack', age=40, ignored_key='nothing')
        entity = SampleEntity()
        entity.from_dict(False, **dict_value)


def test_from_dict_with_hidden_column():
    """
    updates the column values of the entity from those
    values that are available in input keyword arguments.
    the hidden field of the entity should also be updated.
    """

    id = 1300
    name = 'jack'
    age = 40
    hidden_field = 'I am hidden'

    dict_value = DTO(id=id, name=name, age=age, hidden_field=hidden_field)
    entity = SampleWithHiddenFieldEntity()
    entity.from_dict(**dict_value)

    assert entity.id == id
    assert entity.name == name
    assert entity.age == age
    assert entity.hidden_field == hidden_field


def test_table_name():
    """
    gets the table name that this entity represents in database.
    """

    entity = SampleWithHiddenFieldEntity()

    assert entity.table_name() == 'sample_with_hidden_field_table'
    assert entity.table_name() == SampleWithHiddenFieldEntity.table_name()


def test_entity_equal():
    """
    compares different entities which are equal in different scenarios.
    """

    entity1 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_1000', name='joe')
    entity2 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_1000', name='adrian')

    assert entity1 == entity2

    entity3 = SampleEntity(id='2000', name='carol')
    entity4 = SampleEntity(id='2000', name='martin')

    assert entity3 == entity4


def test_entity_not_equal():
    """
    compares different entities which are not equal in different scenarios.
    """

    entity1 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_1000', name='adrian')
    entity2 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_2000', name='adrian')

    assert entity1 != entity2

    entity3 = SampleEntity(id='2000', name='carol')
    entity4 = SampleEntity(id='5', name='martin')

    assert entity3 != entity4


def test_entity_hash_equal():
    """
    compares different entities hashes which are equal in different scenarios.
    """

    entity1 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_1000', name='joe')
    entity2 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_1000', name='adrian')

    assert hash(entity1) == hash(entity2)

    entity3 = SampleEntity(id='2000', name='carol')
    entity4 = SampleEntity(id='2000', name='martin')

    assert hash(entity3) == hash(entity4)


def test_entity_hash_not_equal():
    """
    compares different entities hashes which are not equal in different scenarios.
    """

    entity1 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_1000', name='adrian')
    entity2 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_2000', name='adrian')

    assert hash(entity1) != hash(entity2)

    entity3 = SampleEntity(id='2000', name='carol')
    entity4 = SampleEntity(id='5', name='martin')

    assert hash(entity3) != hash(entity4)

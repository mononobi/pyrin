# -*- coding: utf-8 -*-
"""
model test_services module.
"""

import pytest

from sqlalchemy import Integer, Unicode

from pyrin.core.globals import SECURE_TRUE, SECURE_FALSE
from pyrin.core.structs import DTO
from pyrin.database.model.base import CoreEntity
from pyrin.database.model.exceptions import ColumnNotExistedError
from pyrin.database.orm.sql.schema.base import CoreColumn

from tests.unit.common.models import SampleEntity, SampleWithHiddenFieldEntity, \
    RightChildEntity, LeftChildEntity, BaseEntity, SubBaseEntity, SampleTestEntity


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

    entity = SampleEntity(id=1000, age=20, name='sample', populate_all=SECURE_TRUE)

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
        SampleEntity(id=1000, age=20, name='sample',
                     invalid_kwarg=True, populate_all=SECURE_TRUE,
                     ignore_invalid_column=SECURE_FALSE)


def test_all_columns():
    """
    gets all column names of entity.
    """

    entity1 = SampleWithHiddenFieldEntity()
    fields1 = ['age', 'name', 'hidden_field']

    assert set(fields1) == set(entity1.all_columns)

    entity2 = BaseEntity()
    fields2 = []

    assert set(fields2) == set(entity2.all_columns)

    entity3 = SubBaseEntity()
    fields3 = ['age']

    assert set(fields3) == set(entity3.all_columns)

    entity4 = RightChildEntity()
    fields4 = ['age', 'grade']

    assert set(fields4) == set(entity4.all_columns)


def test_readable_columns():
    """
    gets readable column names of entity.
    readable columns are those that have `allow_read=True`
    """

    entity1 = SampleWithHiddenFieldEntity()
    fields1 = ['age', 'name']

    assert set(fields1) == set(entity1.readable_columns)

    entity2 = BaseEntity()
    fields2 = []

    assert set(fields2) == set(entity2.readable_columns)

    entity3 = SubBaseEntity()
    fields3 = ['age']

    assert set(fields3) == set(entity3.readable_columns)

    entity4 = RightChildEntity()
    fields4 = ['age', 'grade']

    assert set(fields4) == set(entity4.readable_columns)


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
    the result dict only contains the readable columns of
    the entity which are those that their `allow_read` attribute
    is set to True.
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
    entity.from_dict(**dict_value, populate_all=SECURE_TRUE)

    assert entity.id == id
    assert entity.name == name
    assert entity.age == age
    assert hasattr(entity, 'ignored_key') is False


def test_from_dict_with_invalid_column_and_not_silent():
    """
    updates the column values of the entity from those
    values that are available in input keyword arguments.
    there is some invalid column names and `ignore_invalid_column=False`
    has been set. it should raise an error.
    """

    with pytest.raises(ColumnNotExistedError):
        dict_value = DTO(id=1300, name='jack', age=40, ignored_key='nothing')
        entity = SampleEntity()
        entity.from_dict(ignore_invalid_column=SECURE_FALSE,
                         populate_all=SECURE_TRUE, **dict_value)


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
    entity.from_dict(**dict_value, populate_all=SECURE_TRUE)

    assert entity.id == id
    assert entity.name == name
    assert entity.age == age
    assert entity.hidden_field == hidden_field


def test_table_name():
    """
    gets the table name that this entity represents in database.
    """

    entity = SampleWithHiddenFieldEntity()

    assert entity.table_name == 'sample_with_hidden_field_table'
    assert entity.table_name == SampleWithHiddenFieldEntity.table_name


def test_entity_equal():
    """
    compares different entities which are equal in different scenarios.
    """

    entity1 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_1000',
                                          name='joe', populate_all=SECURE_TRUE)
    entity2 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_1000',
                                          name='adrian', populate_all=SECURE_TRUE)

    assert entity1 == entity2

    entity3 = SampleEntity(id='2000', name='carol', populate_all=SECURE_TRUE)
    entity4 = SampleEntity(id='2000', name='martin', populate_all=SECURE_TRUE)

    assert entity3 == entity4

    right_child1 = RightChildEntity(id=1000, populate_all=SECURE_TRUE)
    left_child1 = LeftChildEntity(id=1000, populate_all=SECURE_TRUE)

    assert right_child1 == left_child1

    base_entity1 = BaseEntity(id=10, populate_all=SECURE_TRUE)
    base_entity2 = BaseEntity(id=10, populate_all=SECURE_TRUE)

    assert base_entity1 == base_entity2

    right_child2 = RightChildEntity(id=1000, populate_all=SECURE_TRUE)
    sub_base_entity1 = SubBaseEntity(id=1000, populate_all=SECURE_TRUE)

    assert right_child2 == sub_base_entity1
    assert sub_base_entity1 == right_child2


def test_entity_not_equal():
    """
    compares different entities which are not equal in different scenarios.
    """

    entity1 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_1000',
                                          name='adrian', populate_all=SECURE_TRUE)
    entity2 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_2000',
                                          name='adrian', populate_all=SECURE_TRUE)

    assert entity1 != entity2

    entity3 = SampleEntity(id='2000', name='carol', populate_all=SECURE_TRUE)
    entity4 = SampleEntity(id='5', name='martin', populate_all=SECURE_TRUE)

    assert entity3 != entity4

    right_child1 = RightChildEntity(id=1000, populate_all=SECURE_TRUE)
    left_child1 = LeftChildEntity(id=2000, populate_all=SECURE_TRUE)

    assert right_child1 != left_child1

    base_entity1 = BaseEntity(id=20, populate_all=SECURE_TRUE)
    base_entity2 = BaseEntity(id=10, populate_all=SECURE_TRUE)

    assert base_entity1 != base_entity2

    right_child2 = RightChildEntity(id=2000, populate_all=SECURE_TRUE)
    sub_base_entity1 = SubBaseEntity(id=1000, populate_all=SECURE_TRUE)

    assert right_child2 != sub_base_entity1
    assert sub_base_entity1 != right_child2

    different_entity1 = SampleTestEntity(id=1000, populate_all=SECURE_TRUE)
    different_entity2 = RightChildEntity(id=1000, populate_all=SECURE_TRUE)

    assert different_entity1 != different_entity2


def test_entity_hash_equal():
    """
    compares different entities hashes which are equal in different scenarios.
    """

    entity1 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_1000',
                                          name='joe', populate_all=SECURE_TRUE)
    entity2 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_1000',
                                          name='adrian', populate_all=SECURE_TRUE)

    assert hash(entity1) == hash(entity2)

    entity3 = SampleEntity(id='2000', name='carol', populate_all=SECURE_TRUE)
    entity4 = SampleEntity(id='2000', name='martin', populate_all=SECURE_TRUE)

    assert hash(entity3) == hash(entity4)

    right_child1 = RightChildEntity(id=1000, populate_all=SECURE_TRUE)
    left_child1 = LeftChildEntity(id=1000, populate_all=SECURE_TRUE)

    assert hash(right_child1) == hash(left_child1)

    base_entity1 = BaseEntity(id=10, populate_all=SECURE_TRUE)
    base_entity2 = BaseEntity(id=10, populate_all=SECURE_TRUE)

    assert hash(base_entity1) == hash(base_entity2)

    right_child2 = RightChildEntity(id=1000, populate_all=SECURE_TRUE)
    sub_base_entity1 = SubBaseEntity(id=1000, populate_all=SECURE_TRUE)

    assert hash(right_child2) == hash(sub_base_entity1)


def test_entity_hash_not_equal():
    """
    compares different entities hashes which are not equal in different scenarios.
    """

    entity1 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_1000',
                                          name='adrian', populate_all=SECURE_TRUE)
    entity2 = SampleWithHiddenFieldEntity(id=1000, sub_id='sub_2000',
                                          name='adrian', populate_all=SECURE_TRUE)

    assert hash(entity1) != hash(entity2)

    entity3 = SampleEntity(id='2000', name='carol', populate_all=SECURE_TRUE)
    entity4 = SampleEntity(id='5', name='martin', populate_all=SECURE_TRUE)

    assert hash(entity3) != hash(entity4)

    right_child1 = RightChildEntity(id=1000, populate_all=SECURE_TRUE)
    left_child1 = LeftChildEntity(id=2000, populate_all=SECURE_TRUE)

    assert hash(right_child1) != hash(left_child1)

    base_entity1 = BaseEntity(id=20, populate_all=SECURE_TRUE)
    base_entity2 = BaseEntity(id=10, populate_all=SECURE_TRUE)

    assert hash(base_entity1) != hash(base_entity2)

    right_child2 = RightChildEntity(id=2000, populate_all=SECURE_TRUE)
    sub_base_entity1 = SubBaseEntity(id=1000, populate_all=SECURE_TRUE)

    assert hash(right_child2) != hash(sub_base_entity1)

    different_entity1 = SampleTestEntity(id=1000, populate_all=SECURE_TRUE)
    different_entity2 = RightChildEntity(id=1000, populate_all=SECURE_TRUE)

    assert hash(different_entity1) != hash(different_entity2)


def test_entity_with_schema_table_fullname():
    """
    checks whether schema name is reflected in table fullname.
    note that sqlite does not support schemas, so we have to define
    this entity inside this method to prevent from adding it to
    `CoreEntity.metadata` which produces an error on sqlite.
    """

    class SampleWithSchemaEntity(CoreEntity):
        """
        sample with schema entity class.
        """

        _table = 'sample_with_schema_table'
        _schema = 'my_schema'

        id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
        sub_id = CoreColumn(name='sub_id', type_=Unicode, primary_key=True)

    entity = SampleWithSchemaEntity(id=10, sub_id='sub_10', populate_all=SECURE_TRUE)

    assert entity.table_fullname == 'my_schema.sample_with_schema_table'
    assert entity.table_name == 'sample_with_schema_table'
    assert entity.table_schema == 'my_schema'


def test_entity_without_schema_table_fullname():
    """
    checks whether schema name is not reflected in table fullname.
    """

    entity = BaseEntity(id=10)

    assert entity.table_fullname == entity.table_name
    assert entity.table_schema is None

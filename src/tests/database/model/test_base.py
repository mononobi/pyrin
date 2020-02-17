# -*- coding: utf-8 -*-
"""
model test_services module.
"""

import pytest

from sqlalchemy import Integer, Unicode

from pyrin.core.context import DTO
from pyrin.database.model.base import CoreEntity
from pyrin.database.model.exceptions import ColumnNotExistedError
from pyrin.database.model.schema import CoreColumn

from tests.common.models import SampleEntity, SampleWithHiddenFieldEntity, RightChildEntity, \
    LeftChildEntity, BaseEntity, SubBaseEntity, SampleTestEntity


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

    entity1 = SampleWithHiddenFieldEntity()
    fields1 = ['age', 'sub_id', 'id', 'name', 'hidden_field']

    assert set(fields1) == set(entity1.all_columns())

    entity2 = BaseEntity()
    fields2 = ['id']

    assert set(fields2) == set(entity2.all_columns())

    entity3 = SubBaseEntity()
    fields3 = ['id', 'age']

    assert set(fields3) == set(entity3.all_columns())

    entity4 = RightChildEntity()
    fields4 = ['id', 'age', 'grade']

    assert set(fields4) == set(entity4.all_columns())


def test_exposed_columns():
    """
    gets exposed column names of entity.
    exposed columns are those that have `exposed=True`
    """

    entity1 = SampleWithHiddenFieldEntity()
    fields1 = ['age', 'id', 'sub_id', 'name']

    assert set(fields1) == set(entity1.exposed_columns())

    entity2 = BaseEntity()
    fields2 = ['id']

    assert set(fields2) == set(entity2.exposed_columns())

    entity3 = SubBaseEntity()
    fields3 = ['id', 'age']

    assert set(fields3) == set(entity3.exposed_columns())

    entity4 = RightChildEntity()
    fields4 = ['id', 'age', 'grade']

    assert set(fields4) == set(entity4.exposed_columns())


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

    right_child1 = RightChildEntity(id=1000)
    left_child1 = LeftChildEntity(id=1000)

    assert right_child1 == left_child1

    base_entity1 = BaseEntity(id=10)
    base_entity2 = BaseEntity(id=10)

    assert base_entity1 == base_entity2

    right_child2 = RightChildEntity(id=1000)
    sub_base_entity1 = SubBaseEntity(id=1000)

    assert right_child2 == sub_base_entity1
    assert sub_base_entity1 == right_child2


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

    right_child1 = RightChildEntity(id=1000)
    left_child1 = LeftChildEntity(id=2000)

    assert right_child1 != left_child1

    base_entity1 = BaseEntity(id=20)
    base_entity2 = BaseEntity(id=10)

    assert base_entity1 != base_entity2

    right_child2 = RightChildEntity(id=2000)
    sub_base_entity1 = SubBaseEntity(id=1000)

    assert right_child2 != sub_base_entity1
    assert sub_base_entity1 != right_child2

    different_entity1 = SampleTestEntity(id=1000)
    different_entity2 = RightChildEntity(id=1000)

    assert different_entity1 != different_entity2


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

    right_child1 = RightChildEntity(id=1000)
    left_child1 = LeftChildEntity(id=1000)

    assert hash(right_child1) == hash(left_child1)

    base_entity1 = BaseEntity(id=10)
    base_entity2 = BaseEntity(id=10)

    assert hash(base_entity1) == hash(base_entity2)

    right_child2 = RightChildEntity(id=1000)
    sub_base_entity1 = SubBaseEntity(id=1000)

    assert hash(right_child2) == hash(sub_base_entity1)


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

    right_child1 = RightChildEntity(id=1000)
    left_child1 = LeftChildEntity(id=2000)

    assert hash(right_child1) != hash(left_child1)

    base_entity1 = BaseEntity(id=20)
    base_entity2 = BaseEntity(id=10)

    assert hash(base_entity1) != hash(base_entity2)

    right_child2 = RightChildEntity(id=2000)
    sub_base_entity1 = SubBaseEntity(id=1000)

    assert hash(right_child2) != hash(sub_base_entity1)

    different_entity1 = SampleTestEntity(id=1000)
    different_entity2 = RightChildEntity(id=1000)

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

        __tablename__ = 'sample_with_schema_table'
        __table_args__ = DTO(schema='my_schema')

        id = CoreColumn(name='id', type_=Integer, primary_key=True, autoincrement=False)
        sub_id = CoreColumn(name='sub_id', type_=Unicode, primary_key=True)

        def primary_key(self):
            """
            gets the primary key value of this table.

            :returns tuple(int, str)
            :rtype: tuple
            """

            return self.id, self.sub_id

    entity = SampleWithSchemaEntity(id=10, sub_id='sub_10')

    assert entity.table_fullname() == 'my_schema.sample_with_schema_table'
    assert entity.table_name() == 'sample_with_schema_table'
    assert entity.table_schema() == 'my_schema'


def test_entity_without_schema_table_fullname():
    """
    checks whether schema name is not reflected in table fullname.
    """

    entity = BaseEntity(id=10)

    assert entity.table_fullname() == entity.table_name()
    assert entity.table_schema() is None

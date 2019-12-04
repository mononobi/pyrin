# -*- coding: utf-8 -*-
"""
utils test_sqlalchemy module.
"""

import pyrin.utils.sqlalchemy as sqlalchemy_utils

from pyrin.core.context import DTO

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
    name = 'no name'
    age = 32
    hidden_field = 'I am hidden.'

    entity = SampleWithHiddenFieldEntity()
    entity.id = id
    entity.name = name
    entity.age = age
    entity.hidden_field = hidden_field

    result = sqlalchemy_utils.entity_to_dict(entity)

    assert isinstance(result, dict) is True
    assert len(result) == 3
    assert result['id'] == id
    assert result['name'] == name
    assert result['age'] == age
    assert 'hidden_field' not in result.keys()


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

    entities = []
    entities.append(entity1)
    entities.append(entity2)
    entities.append(entity3)

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

    entities = []
    entities.append(entity1)

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

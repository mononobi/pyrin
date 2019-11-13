# -*- coding: utf-8 -*-
"""
utils test_sqlalchemy module.
"""

import pyrin.utils.sqlalchemy as sqlalchemy_utils

from pyrin.core.context import DTO

from tests.common.models import SampleEntity


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


def test_dict_to_entity():
    """
    converts the given dict into an specified entity and returns it.
    """

    id = 1300
    name = 'jack'
    age = 40

    dict_value = DTO(id=id, name=name, age=age, ignored_key='nothing')
    entity = sqlalchemy_utils.dict_to_entity(dict_value, SampleEntity)

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

    entity = sqlalchemy_utils.dict_to_entity(None, SampleEntity)

    assert entity is not None
    assert entity.id is None
    assert entity.name is None
    assert entity.age is None

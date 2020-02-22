# -*- coding: utf-8 -*-
"""
serializer test_keyed_tuple module.
"""

import pyrin.utils.sqlalchemy as sqlalchemy_utils

from pyrin.converters.serializer.keyed_tuple import CoreKeyedTupleSerializer


def test_serialize():
    """
    serializes the given row result into dict.
    """

    row = sqlalchemy_utils.create_row_result(['id', 'name', 'age'], [1, 'jack', 20])
    result = CoreKeyedTupleSerializer.serialize(row)

    assert isinstance(result, dict)
    assert len(result) == 3
    assert result.get('name', None) == 'jack'
    assert result.get('id', None) == 1
    assert result.get('age', None) == 20


def test_serialize_none():
    """
    serializes the given row result into dict.
    the row result is None so it should return an empty dict.
    """

    result = CoreKeyedTupleSerializer.serialize(None)

    assert isinstance(result, dict)
    assert len(result) == 0


def test_serialize_list():
    """
    serializes the given row result list into dict list.
    """

    row1 = sqlalchemy_utils.create_row_result(['id', 'grade', 'age'], [1, 15, 11])
    row2 = sqlalchemy_utils.create_row_result(['id', 'grade', 'age'], [2, 35, 25])
    row3 = sqlalchemy_utils.create_row_result(['id', 'grade', 'age'], [3, 45, 30])
    values = [row1, row2, row3]
    results = CoreKeyedTupleSerializer.serialize_list(values)

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


def test_serialize_list_none():
    """
    serializes the given row result list into dict list.
    the given list is None, so it should return an empty list.
    """

    results = CoreKeyedTupleSerializer.serialize_list(None)

    assert isinstance(results, list)
    assert len(results) == 0


def test_serialize_list_empty():
    """
    serializes the given row result list into dict list.
    the given list is empty, so it should return an empty list.
    """

    results = CoreKeyedTupleSerializer.serialize_list([])

    assert isinstance(results, list)
    assert len(results) == 0


def test_serialize_list_with_none_values():
    """
    serializes the given row result list into dict list.
    the given list contains None values, so it should
    return a list of empty dicts.
    """

    results = CoreKeyedTupleSerializer.serialize_list([None, None])

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
    serializes the given row result list into dict list.
    the list contains some row results and some None items.
    """

    row1 = sqlalchemy_utils.create_row_result(['id', 'grade', 'age'], [1, 15, 11])
    row2 = None
    row3 = sqlalchemy_utils.create_row_result(['id', 'grade', 'age'], [3, 45, 30])
    values = [row1, row2, row3]
    results = CoreKeyedTupleSerializer.serialize_list(values)

    assert isinstance(results, list)
    assert len(results) == 3

    first = results[0]
    second = results[1]
    third = results[2]

    assert isinstance(first, dict)
    assert isinstance(second, dict)
    assert isinstance(third, dict)

    assert len(first) == 3
    assert len(second) == 0
    assert len(third) == 3

    assert first.get('grade', None) == 15
    assert first.get('id', None) == 1
    assert first.get('age', None) == 11
    assert third.get('grade', None) == 45
    assert third.get('id', None) == 3
    assert third.get('age', None) == 30

# -*- coding: utf-8 -*-
"""
utils test_sqlalchemy module.
"""

import pytest

import pyrin.utils.sqlalchemy as sqlalchemy_utils

from pyrin.utils.exceptions import FieldsAndValuesCountMismatchError, \
    InvalidRowResultFieldsAndValuesError


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

    assert result is None


def test_like_prefix():
    """
    gets a copy of string with `%` attached to beginning
    of it to use in like operator.
    """

    value = 'sample_string'
    result = sqlalchemy_utils.like_prefix(value)

    assert result == '%sample_string'


def test_like_prefix_with_none_value():
    """
    gets a copy of string which is None with `%` attached
    to beginning of it to use in like operator.
    """

    result = sqlalchemy_utils.like_prefix(None)

    assert result is None


def test_like_suffix():
    """
    gets a copy of string with `%` attached to end
    of it to use in like operator.
    """

    value = 'sample_string'
    result = sqlalchemy_utils.like_suffix(value)

    assert result == 'sample_string%'


def test_like_suffix_with_none_value():
    """
    gets a copy of string which is None with `%` attached
    to end of it to use in like operator.
    """

    result = sqlalchemy_utils.like_suffix(None)

    assert result is None


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

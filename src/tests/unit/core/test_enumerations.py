# -*- coding: utf-8 -*-
"""
core test_enumerations module.
"""

from pyrin.core.enumerations import HTTPMethodEnum, RedirectionResponseCodeEnum


def test_values():
    """
    gets all available values of given enumeration.
    """

    values = {'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'TRACE', 'OPTIONS',
              'PATCH', 'COPY', 'LINK', 'UNLINK', 'PURGE', 'VIEW'}

    enum_values = HTTPMethodEnum.values()

    assert len(values) == len(enum_values)
    assert values == set(enum_values)


def test_contains():
    """
    checks that given value is existed in the enumeration.
    """

    assert HTTPMethodEnum.contains('GET')
    assert HTTPMethodEnum.contains('UNLINK')
    assert RedirectionResponseCodeEnum.contains(302)
    assert not HTTPMethodEnum.contains('unlink')
    assert not HTTPMethodEnum.contains('COPY2')
    assert not RedirectionResponseCodeEnum.contains(500)


def test_in():
    """
    checks that given value is existed in the enumeration using `in` keyword.
    """

    assert 'GET' in HTTPMethodEnum
    assert 'UNLINK' in HTTPMethodEnum
    assert 301 in RedirectionResponseCodeEnum
    assert 'unlink' not in HTTPMethodEnum
    assert 'COPY2' not in HTTPMethodEnum
    assert 400 not in RedirectionResponseCodeEnum

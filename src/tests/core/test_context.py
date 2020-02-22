# -*- coding: utf-8 -*-
"""
core test_context module.
"""

from pyrin.core.context import DTO, Manager, Hook, CLI


def test_dto_equal():
    """
    compares different DTO objects which are equal in different scenarios.
    """

    data1 = DTO(a=1, b=2, c=3)
    data2 = DTO(b=2, a=1, c=3)

    assert data1 == data2

    data3 = DTO(a=20, b=30, c=40)
    data4 = DTO(a=20, b=30, c=40)

    assert data3 == data4

    data5 = DTO(b=30, a=data1, c=data3)
    data6 = DTO(c=data4, a=data2, b=30)

    assert data5 == data6

    data7 = DTO()
    data8 = DTO()

    assert data7 == data8

    data9 = DTO()
    data9[data1] = data1

    data10 = DTO()
    data10[data2] = data2

    assert data9 == data10

    data11 = DTO()
    data11[data5] = data5

    data12 = DTO()
    data12[data6] = data6

    assert data11 == data12

    value1 = DTO(x=data11, y=data5)
    value2 = DTO(y=data6, x=data12)

    data13 = DTO(z=90, u=value1)
    data13[data11] = data11

    data14 = DTO(z=90, u=value2)
    data14[data12] = data12

    assert value1 == value2
    assert data13 == data14


def test_dto_not_equal():
    """
    compares different DTO objects which are not equal in different scenarios.
    """

    data1 = DTO(a=1, b=2, c=3)
    data2 = DTO(b=2, A=1, c=3)

    assert data1 != data2

    data3 = DTO(a=20, b=30, c=40)
    data4 = DTO(a=20, b=30, c=40, z=50)

    assert data3 != data4

    data5 = DTO(b=30, a=data1, c=data3)
    data6 = DTO(c=data4, a=data2, b=30)

    assert data5 != data6

    data9 = DTO()
    data9[data1] = data1

    data10 = DTO()
    data10[data2] = data2

    assert data9 != data10

    data11 = DTO()
    data11[data5] = data5

    data12 = DTO()
    data12[data5] = data6

    assert data11 != data12

    data_equal1 = DTO(b=3, a=1)
    data_equal1[data1] = data1

    data_equal2 = DTO(a=1, b=3)
    data_equal2[data1] = data1

    assert data_equal1 != data_equal2

    value1 = DTO(x=data_equal1, y=data_equal2)
    value2 = DTO(y=data_equal2, x=data_equal1)

    assert value1 == value2

    data13 = DTO(z=90, u=value1)
    data13[data_equal1] = data_equal1

    data14 = DTO(u=value1, z=90)
    data14[data_equal1] = data_equal1

    assert data13 != data14


def test_manager_is_singleton():
    """
    tests that different types of managers are singleton.
    """

    manager1 = Manager()
    manager2 = Manager()

    assert manager1 == manager2


def test_hook_is_singleton():
    """
    tests that different types of hooks are singleton.
    """

    hook1 = Hook()
    hook2 = Hook()

    assert hook1 == hook2


def test_cli_is_singleton():
    """
    tests that different types of cli classes are singleton.
    """

    cli1 = CLI()
    cli2 = CLI()

    assert cli1 == cli2

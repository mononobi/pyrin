# -*- coding: utf-8 -*-
"""
caching test_structs module.
"""

from pyrin.caching.structs import CacheableDict


def test_cacheable_dict_equal():
    """
    compares different cacheable dict objects which are equal in different scenarios.
    """

    data1 = CacheableDict(a=1, b=2, c=3)
    data2 = CacheableDict(b=2, a=1, c=3)

    assert data1 == data2

    data3 = CacheableDict(a=20, b=30, c=40)
    data4 = CacheableDict(a=20, b=30, c=40)

    assert data3 == data4

    data5 = CacheableDict(b=30, a=data1, c=data3)
    data6 = CacheableDict(c=data4, a=data2, b=30)

    assert data5 == data6

    data7 = CacheableDict()
    data8 = CacheableDict()

    assert data7 == data8

    data9 = CacheableDict()
    data9[data1] = data1

    data10 = CacheableDict()
    data10[data2] = data2

    assert data9 == data10

    data11 = CacheableDict()
    data11[data5] = data5

    data12 = CacheableDict()
    data12[data6] = data6

    assert data11 == data12

    value1 = CacheableDict(x=data11, y=data5)
    value2 = CacheableDict(y=data6, x=data12)

    data13 = CacheableDict(z=90, u=value1)
    data13[data11] = data11

    data14 = CacheableDict(z=90, u=value2)
    data14[data12] = data12

    assert value1 == value2
    assert data13 == data14


def test_cacheable_dict_not_equal():
    """
    compares different cacheable dict objects which are not equal in different scenarios.
    """

    data1 = CacheableDict(a=1, b=2, c=3)
    data2 = CacheableDict(b=2, A=1, c=3)

    assert data1 != data2

    data3 = CacheableDict(a=20, b=30, c=40)
    data4 = CacheableDict(a=20, b=30, c=40, z=50)

    assert data3 != data4

    data5 = CacheableDict(b=30, a=data1, c=data3)
    data6 = CacheableDict(c=data4, a=data2, b=30)

    assert data5 != data6

    data9 = CacheableDict()
    data9[data1] = data1

    data10 = CacheableDict()
    data10[data2] = data2

    assert data9 != data10

    data11 = CacheableDict()
    data11[data5] = data5

    data12 = CacheableDict()
    data12[data5] = data6

    assert data11 != data12

    data_equal1 = CacheableDict(b=3, a=1)
    data_equal1[data1] = data1

    data_equal2 = CacheableDict(a=1, b=3)
    data_equal2[data1] = data1

    value1 = CacheableDict(x=data_equal1, y=data_equal2)
    value2 = CacheableDict(y=data_equal2, x=data_equal1)

    assert value1 == value2

    data13 = CacheableDict(z=90, u=value1)
    data13[data_equal1] = data_equal1

# -*- coding: utf-8 -*-
"""
database utils pool module.
"""

from sqlalchemy.pool import Pool, NullPool, AssertionPool, QueuePool, \
    SingletonThreadPool, StaticPool

from pyrin.core.exceptions import CoreNameError


def get_pool_class(name):
    """
    gets pool class from given pool class name.

    :param str name: name of pool class to get.

    :raises CoreNameError: core name error.

    :rtype: Pool
    """

    try:
        return eval(name)
    except Exception as error:
        raise CoreNameError('Pool class [{name}] does not exist.'
                            .format(name=name)) from error

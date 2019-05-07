# -*- coding: utf-8 -*-
"""
logging decorators module.
"""

import time

from pyrin.settings.logging import AUDIT_LOG

total = 0
count = 0


def audit(func):
    """
    decorator to log information before and after a function execution.

    :param callable func: function.

    :returns: function result.
    """

    def decorator(*args, **kwargs):
        """
        decorates the given function and logs it's behavior
        and returns the function's result every time that function gets called.

        :param object args: function arguments.
        :param object kwargs: function keyword arguments.

        :returns: function result.
        """

        if not AUDIT_LOG:
            return func(*args, **kwargs)

        start_time = time.time()
        try:
            # do some logging here.
            return func(*args, **kwargs)

        except Exception as ex:
            # do some error logging here.
            raise ex
        finally:
            end_time = time.time()
            print('duration of function call [{name}]: {seconds} sec'.
                  format(name=func.__name__, seconds=((end_time - start_time) * 1000)))
            # do some logging here.
            global total
            total += ((end_time - start_time) * 1000)
            global count
            count += 1

            print('COUNT: ', count, ' TOTAL: ', total, ' sec')

    return decorator

# -*- coding: utf-8 -*-
"""
logging decorators module.
"""

import time

from functools import update_wrapper

from pyrin.settings.static import AUDIT_LOG
from pyrin.utils.custom_print import print_info

total = 0
count = 0


def audit(func):
    """
    decorator to log information before and after
    a function execution in debug mode.

    :param callable func: function.

    :returns: function result.
    """

    def decorator(*args, **kwargs):
        """
        decorates the given function and logs it's behavior in debug mode
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
            print_info('Duration of function call [{name}]: {milliseconds} ms'.
                       format(name=func.__name__, milliseconds=(end_time - start_time) * 1000))
            # do some logging here.
            global total
            total += (end_time - start_time) * 1000
            global count
            count += 1

            print_info('COUNT: {count} TOTAL: {total} ms'.format(count=count, total=total))

    return update_wrapper(decorator, func)

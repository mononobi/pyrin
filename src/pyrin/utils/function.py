# -*- coding: utf-8 -*-
"""
utils function module.
"""

import inspect


def get_doc(func, include_returns=True):
    """
    gets docstring of given function.

    :param function func: function to get its docstring.

    :param bool include_returns: specifies that `returns` and `rtype` parts
                                 of docstring must also be included in the result.
                                 defaults to True if not provided.

    :rtype: str
    """

    value = inspect.getdoc(func)
    if value is None:
        return None

    if include_returns is False:
        return_key = ':return'
        rtype_key = ':rtype'

        not_found_index = 5000000
        return_key_index = not_found_index
        rtype_key_index = not_found_index

        if return_key in value:
            return_key_index = value.index(return_key)

        if rtype_key in value:
            rtype_key_index = value.index(rtype_key)

        last_index = min(return_key_index, rtype_key_index)

        if last_index < not_found_index:
            value = value[0:last_index]

    return value

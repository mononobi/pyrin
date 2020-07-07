# -*- coding: utf-8 -*-
"""
utils function module.
"""

import inspect

import pyrin.utils.misc as misc_utils

from pyrin.utils.exceptions import IsNotUserDefinedFunctionError


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


def get_fully_qualified_name(func):
    """
    gets the fully qualified name of given function.

    it returns `module_name.function_name`.
    for example: `pyrin.api.services.create_route`.

    :param function func: function to get its fully qualified name.

    :raises IsNotUserDefinedFunctionError: is not user defined function error.

    :rtype: str
    """

    if not inspect.isfunction(func):
        raise IsNotUserDefinedFunctionError('The provided parameter [{function}] is not a '
                                            'user defined function. use the method '
                                            '"pyrin.utils.misc.try_get_fully_qualified_name" '
                                            'for other object types.')

    return misc_utils.try_get_fully_qualified_name(func)

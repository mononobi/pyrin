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
                          it must be a stand-alone function, not an
                          instance or class method.

    :raises IsNotUserDefinedFunctionError: is not user defined function error.

    :rtype: str
    """

    if not inspect.isfunction(func):
        raise IsNotUserDefinedFunctionError('The provided parameter [{function}] is not a '
                                            'user defined stand-alone function. use the method '
                                            '"pyrin.utils.misc.try_get_fully_qualified_name" '
                                            'for other object types.')

    return misc_utils.try_get_fully_qualified_name(func)


def get_inputs(func, args, kwargs, container=dict, **options):
    """
    gets given function inputs as a dict from provided args and kwargs.

    :param function func: function to get its inputs.
    :param tuple args: a tuple of function positional inputs.
    :param dict kwargs: a dictionary of function keyword arguments.
    :param type container: a dict like object to be used for returning inputs.
                           defaults to dict if not provided.

    :keyword bool remove_self: specifies that `self` parameter must be
                               removed from inputs. defaults to False
                               if not provided.

    :keyword bool remove_cls: specifies that `cls` parameter must be
                              removed from inputs. defaults to False
                              if not provided.

    :rtype: dict
    """

    if len(args) == 0 and len(kwargs) == 0:
        return container()

    remove_self = options.get('remove_self', False)
    remove_cls = options.get('remove_cls', False)

    signature = inspect.signature(func)
    bounded_args = signature.bind_partial(*args, **kwargs)
    inputs = dict(bounded_args.arguments, **bounded_args.kwargs)

    if remove_self is True:
        inputs.pop('self', None)

    if remove_cls is True:
        inputs.pop('cls', None)

    return container(inputs)

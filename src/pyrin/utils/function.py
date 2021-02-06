# -*- coding: utf-8 -*-
"""
utils function module.
"""

import inspect

from inspect import Parameter


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

    :rtype: str
    """

    return '{module}.{name}'.format(module=func.__module__, name=func.__name__)


def get_inputs(func, args, kwargs, container=dict, **options):
    """
    gets given function inputs as a dict from provided args and kwargs.

    it also returns the parent class or instance of function if available.

    :param function func: function to get its inputs.
    :param tuple args: a tuple of function positional inputs.
    :param dict kwargs: a dictionary of function keyword arguments.
    :param type container: a dict like object to be used for returning inputs.
                           defaults to dict if not provided.

    :returns: tuple[dict inputs, object | type parent]
    :rtype: tuple[dict, object | type]
    """

    if len(args) == 0 and len(kwargs) == 0:
        return container(), None

    kwargs_name = None
    signature = inspect.signature(func)
    for name, param in signature.parameters.items():
        if param.kind == Parameter.VAR_KEYWORD:
            kwargs_name = name
            break

    bounded_args = signature.bind_partial(*args, **kwargs)
    parent = bounded_args.arguments.pop('self', None)
    parent = bounded_args.arguments.pop('cls', parent)

    if kwargs_name is not None:
        keywords = bounded_args.arguments.pop(kwargs_name, None)
        if keywords is not None:
            bounded_args.arguments.update(keywords)

    return container(bounded_args.arguments), parent


def get_required_arguments(func):
    """
    gets all required arguments of given function.

    :param function func: function to get its required arguments names.

    :rtype: set[str]
    """

    signature = inspect.signature(func)
    result = []
    for name, item in signature.parameters.items():
        if item.kind in (Parameter.POSITIONAL_ONLY,
                         Parameter.POSITIONAL_OR_KEYWORD,
                         Parameter.KEYWORD_ONLY):

            if item.default is Parameter.empty:
                result.append(name)

    return set(result)


def apply(func, args, kwargs):
    """
    a helper method that applies args and kwargs to given function and gets the result.

    :param function func: function to be used.
    :param tuple args: function positional arguments.
    :param dict kwargs: function keyword arguments.

    :returns: function result
    """

    return func(*args, **kwargs)

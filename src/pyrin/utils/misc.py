# -*- coding: utf-8 -*-
"""
utils misc module.
"""

import inspect

from pyrin.core.globals import LIST_TYPES
from pyrin.core.exceptions import CoreAttributeError


def set_attributes(instance, **kwargs):
    """
    sets the provided keyword arguments as attributes in given object instance.

    :param CoreObject instance: instance to set attributes for.

    :returns: instance with updated attributes.
    :rtype: CoreObject
    """

    if instance is None:
        return instance

    for name, value in kwargs.items():
        if hasattr(instance, name):
            delattr(instance, name)

        setattr(instance, name, value)

    return instance


def extract_attributes(instance, *attributes):
    """
    extracts all attributes with given names from provided object instance.

    :param CoreObject instance: instance to extract attributes from.
    :param attributes: list of all attribute names that should be extracted.

    :raises CoreAttributeError: core attribute error.

    :returns: dict[str name: object value]
    :rtype: dict
    """

    result = dict()
    if instance is None:
        return result

    for name in attributes:
        if not hasattr(instance, name):
            raise CoreAttributeError('Object [{object}] has no attribute [{name}].'
                                     .format(object=str(instance), name=name))
        result[name] = getattr(instance, name)

    return result


def make_iterable(values, collection=None):
    """
    converts the provided values to iterable.

    it returns a collection of values using the given collection type.

    :param object | list[object] | tuple[object] | set[object] values: value or values to make
                                                                       iterable. if the values
                                                                       are iterable, it just
                                                                       converts the collection
                                                                       to given type.

    :param type[list | tuple | set] collection: collection type to use.
                                                defaults to list if not provided.

    :rtype: list | tuple | set
    """

    if collection is None:
        collection = list

    if values is None:
        return collection()

    if not isinstance(values, LIST_TYPES):
        values = (values,)

    return collection(values)


def try_get_fully_qualified_name(some_object):
    """
    tries to get the fully qualified name of given object.

    it tries to return `__module__.__name__` for given object.
    for example: `pyrin.api.services.create_route`.
    but if it fails to get any of those, it returns the `__str__` for that object.

    :param object some_object: object to get its fully qualified name.

    :rtype: str
    """

    module = None
    name = None
    try:
        module = some_object.__module__
        if module == '' or module.isspace():
            module = None
    except AttributeError:
        module = None

    try:
        name = some_object.__name__
        if name == '' or name.isspace():
            name = None
    except AttributeError:
        name = None

    if module is not None and name is not None:
        return '{module}.{name}'.format(module=module, name=name)

    return str(some_object)


def iterate_items(collection, *args, **kwargs):
    """
    iterates over the items of given object.

    :param type collection: collection type to be used to
                            iterate over given object's items.

    :rtype: iterator[tuple[object, object]]
    """

    return iter(collection.items(*args, **kwargs))


def is_subclass_or_instance(value, type_):
    """
    gets a value indicating that given value is an instance or subclass of given type.

    :param object | type value: value to be checked.
    :param type type_: type to be used.

    :rtype: bool
    """

    is_subclass = inspect.isclass(value) and issubclass(value, type_)
    return is_subclass or isinstance(value, type_)

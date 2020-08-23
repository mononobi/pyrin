# -*- coding: utf-8 -*-
"""
caching key providers module.
"""

import pyrin.security.session.services as session_services
import pyrin.utils.function as func_utils

from pyrin.core.structs import CoreObject


class KeyProviderBase(CoreObject):
    """
    key provider base class.

    all caching key providers must be subclassed from this.
    """

    def __init__(self, func, args, kwargs):
        """
        initializes an instance of KeyProviderBase.

        :param function func: function to be cached.
        :param tuple args: a tuple of function positional inputs.
        :param dict kwargs: a dictionary of function keyword arguments.
        """

        super().__init__()

        self._key = self._generate_key(func, args, kwargs)

    def __hash__(self):
        """
        gets the hash of current key.

        :rtype: int
        """

        return hash(self._key)

    def _generate_key(self, func, args, kwargs):
        """
        generates cache key for given function.

        it returns a tuple of four values. instance type, function name,
        function inputs as a dict and current component key.

        note that instance type is None for standalone functions.

        :param function func: function to generate cache key from it.
        :param tuple args: a tuple of function positional inputs.
        :param dict kwargs: a dictionary of function keyword arguments.

        :returns: tuple[type instance_type, str name, dict inputs, object component_key]
        :rtype: tuple[type, str, dict, object]
        """

        name = self._get_function_name(func)
        inputs = self._get_function_inputs(func, args, kwargs)
        component_key = self._get_component_key()
        found_type = self._get_type(inputs)

        return found_type, name, inputs, component_key

    def _get_type(self, inputs):
        """
        gets the type from `self` or `cls` if available in inputs.

        otherwise returns None.
        this method is intended to be overridden in subclasses

        :param dict inputs: inputs to get value from.

        :rtype: type
        """

        return None

    def _get_function_name(self, func):
        """
        gets given function name.

        it returns fully qualified name of function if available.
        otherwise returns the function name itself.

        :param function func: function to get its name.

        :rtype: str
        """

        return func_utils.get_fully_qualified_name(func)

    def _get_function_inputs(self, func, args, kwargs):
        """
        gets a dict of all function passed inputs.

        :param function func: function to get its inputs.
        :param tuple args: a tuple of function positional inputs.
        :param dict kwargs: a dictionary of function keyword arguments.

        :rtype: dict
        """

        return func_utils.get_inputs(func, args, kwargs)

    def _get_component_key(self):
        """
        gets current component key.

        it returns None if component key is not available.

        :rtype: object
        """

        return session_services.get_safe_component_custom_key()

    @property
    def key(self):
        """
        gets the current cache key.

        :returns: tuple[type instance_type, str name, dict inputs, object component_key]
        :rtype: tuple[type, str, dict, object]
        """

        return self._key


class TypedKeyProvider(KeyProviderBase):
    """
    typed key provider class.

    this class considers type of first argument of instance or class
    level methods for key generation.
    on stand-alone functions, it considers type as None.
    as this provider includes type in key generation, the cached value
    will be shared between all instances of the same type if other cache
    key parts are the same.
    """

    def _get_type(self, inputs):
        """
        gets the type from `self` or `cls` if available in inputs.

        otherwise returns None.

        :param dict inputs: inputs to get value from.

        :rtype: type
        """

        instance = inputs.pop('self', None)
        if instance is not None:
            return type(instance)

        class_type = inputs.pop('cls', None)
        if class_type is not None:
            return class_type

        return None


class KeyProvider(KeyProviderBase):
    """
    key provider class.

    this class does not consider type of first argument of instance or class
    level methods for key generation.
    so it is suitable for instance level or stand-alone function caching.
    """

    def _get_type(self, inputs):
        """
        gets the type from `self` or `cls` if available in inputs.

        otherwise returns None.

        :param dict inputs: inputs to get value from.

        :rtype: type
        """

        inputs.pop('cls', None)
        inputs.pop('self', None)

        return None

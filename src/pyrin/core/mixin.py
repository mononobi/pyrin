# -*- coding: utf-8 -*-
"""
core mixin module.
"""

from pyrin.core.context import CoreObject, Hook
from pyrin.core.exceptions import InvalidHookTypeError


class HookMixin(CoreObject):
    """
    hook mixin class.
    every class that needs to provide hooks must inherit from this.
    """

    _hook_type = Hook

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of HookMixin.
        """

        super().__init__()

        self._hooks = []

    def _get_hooks(self):
        """
        gets all registered hooks.

        :returns: list[Hook]
        :rtype: list
        """

        return self._hooks

    def register_hook(self, instance):
        """
        registers the given instance into hooks.

        :param Hook instance: hook instance to be registered.

        :raises InvalidHookTypeError: invalid hook type error.
        """

        if not isinstance(instance, self._hook_type):
            raise InvalidHookTypeError('Input parameter [{instance}] is '
                                       'not an instance of [{hook}].'
                                       .format(instance=str(instance),
                                               hook=self._hook_type))

        self._hooks.append(instance)

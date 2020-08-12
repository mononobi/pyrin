# -*- coding: utf-8 -*-
"""
core mixin module.
"""

import pyrin.utils.misc as misc_utils

from pyrin.core.structs import CoreObject, Hook
from pyrin.core.exceptions import InvalidHookTypeError


class HookMixin(CoreObject):
    """
    hook mixin class.

    every class that needs to provide hooks must inherit from this.
    """

    hook_type = Hook
    invalid_hook_type_error = InvalidHookTypeError

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

        if not isinstance(instance, self.hook_type):
            full_name = misc_utils.try_get_fully_qualified_name(self.hook_type)
            raise self.invalid_hook_type_error('Input parameter [{instance}] is '
                                               'not an instance of [{hook}].'
                                               .format(instance=instance,
                                                       hook=full_name))
        self._hooks.append(instance)

# -*- coding: utf-8 -*-
"""
core test_mixin module.
"""

import pytest

from pyrin.core.structs import Hook
from pyrin.core.exceptions import InvalidHookTypeError

from tests.unit.core.mixin import HookEnabledMock


def test_get_hooks_attribute():
    """
    tests that hooks attribute is available in hook enabled mock class.
    """

    hook_holder = HookEnabledMock()
    assert hook_holder._get_hooks() == []


def test_register_hook():
    """
    registers given hook.
    """

    hook = Hook()
    hook_holder = HookEnabledMock()
    hook_holder.register_hook(hook)
    hooks = hook_holder._get_hooks()

    assert isinstance(hooks, list)
    assert len(hooks) == 1
    assert hooks[0] == hook
    hooks.clear()


def test_register_hook_invalid_type():
    """
    registers given hook with invalid type.
    it should raise an error.
    """

    hook_holder = HookEnabledMock()

    with pytest.raises(InvalidHookTypeError):
        hook_holder.register_hook(23)

    hooks = hook_holder._get_hooks()
    assert isinstance(hooks, list)
    assert len(hooks) == 0

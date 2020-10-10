# -*- coding: utf-8 -*-
"""
core test_structs module.
"""

from pyrin.core.structs import Manager, Hook, CLI


def test_manager_is_singleton():
    """
    tests that different types of managers are singleton.
    """

    manager1 = Manager()
    manager2 = Manager()

    assert manager1 == manager2


def test_hook_is_singleton():
    """
    tests that different types of hooks are singleton.
    """

    hook1 = Hook()
    hook2 = Hook()

    assert hook1 == hook2


def test_cli_is_singleton():
    """
    tests that different types of cli classes are singleton.
    """

    cli1 = CLI()
    cli2 = CLI()

    assert cli1 == cli2

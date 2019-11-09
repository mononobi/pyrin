# -*- coding: utf-8 -*-
"""
database services module.
"""

from pyrin.application.services import get_component

from tests.database import TestDatabasePackage


def get_binds():
    """
    gets a shallow copy of binds dictionary.

    :returns: dict(type entity: str bind_name)
    :rtype: dict(type: str)
    """

    return get_component(TestDatabasePackage.COMPONENT_NAME).get_binds()


def get_bounded_engines():
    """
    gets a shallow copy of bounded engines dictionary.

    :returns: dict(str bind_name: Engine engine)
    :rtype: dict(str: Engine)
    """

    return get_component(TestDatabasePackage.COMPONENT_NAME).get_bounded_engines()


def get_entity_to_engine_map():
    """
    gets a shallow copy of entity to engine map dictionary.

    :returns: dict(type entity: Engine engine)
    :rtype: dict(type: Engine)
    """

    return get_component(TestDatabasePackage.COMPONENT_NAME).get_entity_to_engine_map()

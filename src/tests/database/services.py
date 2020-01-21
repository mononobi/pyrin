# -*- coding: utf-8 -*-
"""
database services module.
"""

from pyrin.application.services import get_component

from tests.database import DatabasePackage


def get_binds():
    """
    gets a shallow copy of binds dictionary.

    :returns: dict(type entity: str bind_name)
    :rtype: dict
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_binds()


def get_entity_to_engine_map():
    """
    gets a shallow copy of entity to engine map dictionary.

    :returns: dict(type entity: Engine engine)
    :rtype: dict
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_entity_to_engine_map()


def get_engine_to_table_map():
    """
    gets a shallow copy of engine to table map dictionary.

    :returns: dict(Engine engine: list[Table] tables)
    :rtype: dict
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_engine_to_table_map()


def get_all_engines():
    """
    gets all database engines.

    :returns: list[Engine]
    :rtype: list
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_all_engines()


def remove_bind(entity):
    """
    removes the given entity from binds dictionary.

    :param type entity: entity type to be removed.
    """

    return get_component(DatabasePackage.COMPONENT_NAME).remove_bind(entity)

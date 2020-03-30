# -*- coding: utf-8 -*-
"""
database migration test_services module.
"""

import pytest

import pyrin.database.migration.services as migration_services


def test_get_engine_to_table_map():
    """
    gets engine to table map dictionary.
    """
    pass
    # engine_to_table_map = extended_database_services.get_engine_to_table_map()
    # all_engines = extended_database_services.get_all_engines()
    #
    # assert engine_to_table_map is not None
    # assert len(engine_to_table_map) >= 3
    # assert all(engine in engine_to_table_map for engine in all_engines)


@pytest.mark.skip('we should not create database between '
                  'tests, server has created it on startup.')
def test_create_all():
    """
    creates all entities on database engine.
    """

    migration_services.create_all()


@pytest.mark.skip('we should not drop database between '
                  'tests, server will do it at the end.')
def test_drop_all():
    """
    drops all entities on database engine.
    """

    migration_services.drop_all()

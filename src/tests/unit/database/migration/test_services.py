# -*- coding: utf-8 -*-
"""
database migration test_services module.
"""

import pytest

import pyrin.database.migration.services as migration_services


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
